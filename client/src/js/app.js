
var state = {
	sensor_script: '',
	selected: {
		wifi: true,
		camera: ''
	},
	items: []
};

const Home = { 
	template: '#yml-modifier-template',
	data: function() {
		return state
	},
	mounted: async function() {
		// socket.addEventListener('message', (event) => {
		// 	state.items = JSON.parse(event.data).opticals;
		// }); 
		// let res = await axios.get('http://192.168.4.1:6500/opticals');
		// console.log(res);
		// state.items = res.data.opticals;
		let res = await axios.get('http://192.168.4.1:6500/sensorproxy_yml');

		console.log(res);
		state.sensor_script = '\n'+res.data.body.replace(/\\n/g, '\n');
		this.generateScript();
	},
	methods: {
		generateScript: function() {
			// console.log(
			// 	'generateScript',this.selected.camera.value);
			let gs = ''+
			SensorScript.section.cam(this.selected.camera)+
			SensorScript.section.log()+
			(this.selected.wifi ? SensorScript.section.wifi() : '')+
			SensorScript.section.lift();

			// this.sensor_script = gs; 
			// console.log(gs);
		},
		save: async function() {
			let res = await axios.post('http://192.168.4.1:6500/sensorproxy_yml', {
				body: this.sensor_script
			},  {
				headers: { 
					'Content-Type': "application/json",
					"Access-Control-Allow-Origin": "*", 
				}
			});

			console.log(res);
		},
		saveApply: function() {
			
		}
	}
}
const Foo = { 
	template: '#journalctl-logs-template',
	data: function() {
		return {
			logs: ''
		}
	},
	mounted: async function() {
		let ws = new WebSocket('ws://192.168.4.1:6550/journalctl');
		// const reader = new FileReader();
		let logs = sessionStorage.getItem('sensorproxy-logs') ? sessionStorage.getItem('sensorproxy-logs') : '';
		this.logs = '\n'+logs.trim(); 

		console.log({ logs: logs });

		vm = this;
		ws.addEventListener('open', (evt) => {
			console.log('WS: [OPEN]',evt);
		})
		ws.addEventListener('error', (err) => {
			console.log('WS: [ERROR]',err.data);
		})
		ws.addEventListener('message', (evt) => {
			// console.log(evt);
			vm.logs += evt.data+'\n';
		})
		ws.addEventListener('close', (evt) => {
			console.log('WS: [CLOSE]', evt);
		})

		window.onbeforeunload = function() {
			// ws.onclose = function () {}; // disable onclose handler first
			ws.close();
			// console.log(vm.logs);
			sessionStorage.setItem('sensorproxy-logs', vm.logs);
		};
	},
	beforeRouteLeave: function (to, from, next) {
		sessionStorage.setItem('sensorproxy-logs', this.logs);
		console.log(to); 
		console.log(from); 
		next();
	}
}

const router = new VueRouter({
	mode: 'history',
	routes: [
		{ path: '/', component: Home },
		{ path: '/logs', component: Foo }
	]
})

const SensorScript = {
	content: '',
	init : function() {
		this.content = ''
	},
	section: {
		cam: function(type) {
			return type ? '\n'+
				'cam:\n'+                            
				`  type: ${type}\n`+
				'  img_format: jpeg\n'
			: '';
		},		
		log: function() {
			return '\n'+
				'log:\n'+                            
				'  level: info\n'+
				'  file_name: sensorproxy.txt\n';
		},
		wifi: function() {
			return '\n'+
				'wifi:\n'+                            
				'  interface: wlan0\n'+
				'  host_ap: true\n';
		},
		lift: function() {
			return '\n'+
				'lift:\n'+                            
				'  ssid: nature40.liftsystem.709e\n'+
				'  height: 30\n';
		}
	}
}


// const socket = new WebSocket('ws://127.0.0.1:6550/opticals'); 

const app = new Vue({
	router,
	el: '#app',
	data: {
		state: ''
	},
	mounted: async function() {
		this.state = window.location.pathname == '/' ? 'mod' : 'logs';
	},
	methods: {
		changeState(state) {
			this.state = state;
		}
	}
})


$(document).ready(() => {
	$('#app .camera-selector').dropdown();
})
