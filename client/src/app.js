const Home = { template: '<div>Home</div>' }
const Foo = { template: '<div>Foo</div>' }

const router = new VueRouter({
	mode: 'history',
	routes: [
		{ path: '/', component: Home },
		{ path: '/foo', component: Foo }
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

var state = {
	sensor_script: '',
	selected: {
		wifi: true,
		camera: ''
	},
	items: ['Camera 1','Camera 2','Camera 3','Camera 4']
};

// const socket = new WebSocket('ws://127.0.0.1:6550/opticals'); 

const app = new Vue({
	router,
	el: '#app',
	data: state,
	mounted: async function() {
		// socket.addEventListener('message', (event) => {
		// 	state.items = JSON.parse(event.data).opticals;
		// }); 
		let res = await axios.get('http://127.0.0.1:6500/opticals');
		console.log(res);
		state.items = res.data.opticals;
		res = await axios.get('http://127.0.0.1:6500/sensorproxy_yml');
		state.sensor_script = '\n'+res.data;
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
		}
	}
})


$(document).ready(() => {

	$('#app .camera-selector').dropdown();
})