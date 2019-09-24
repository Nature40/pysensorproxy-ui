const YamlModifier = { 
	template: '#yml-modifier-template',
	data: function() {
		return {
			sensorproxy_yml: '',
			editor: null, 
			sensors: {},
			response: {},
			windowHeight: 0,
		}
	},
	created: function() {
		vm = this;
		
		vm.windowHeight = window.innerHeight-40; 
		// console.log(this.windowHeight);
		window.addEventListener('resize', (evt) => {
			vm.windowHeight = evt.target.innerHeight-40;
			// console.log(evt.target);
		})
	},
	mounted: async function() {
		this.editor = ace.edit("editor");
		this.editor.setTheme("ace/theme/eclipse");
		this.editor.session.setMode("ace/mode/yaml");

		let ysp = await fetch('http://192.168.4.1:6500/yml/sensorproxy', {
			method: 'get',
			credentials: 'same-origin',
			mode: 'cors'
		}) 

		let sns = await fetch('http://192.168.4.1:6500/sensors', {
			method: 'get',
			credentials: 'same-origin',
			mode: 'cors'
		}) 

		// let ysp = await axios.get('http://192.168.4.1:6500/yml/sensorproxy');
		// let sns = await axios.get('http://192.168.4.1:6500/sensors');
		
		this.sensorproxy_yml = (await ysp.json()).body.replace(/\\n/g, '\n');
		this.sensors = (await sns.json()).sensors;

		console.log(this.sensors);

		this.editor.session.setValue(this.sensorproxy_yml);

	},
	methods: {
		save: async function() {
			let yml = await fetch('http://192.168.4.1:6500/yml/sensorproxy', {
				method: 'post',
				credentials: 'same-origin',
				mode: 'cors',
				headers: { 
					'Content-Type': "text/plain",
				}, 
				body: JSON.stringify({
					body: this.editor.getValue()
				}),
			})

			this.response = await yml.json();
			vm = this;
			window.setTimeout(() => {
				vm.response = {}
			}, 3000)
		},
		saveApply: async function() {
			let yml = await fetch('http://192.168.4.1:6500/yml/sensorproxy', {
				method: 'post',
				credentials: 'same-origin',
				mode: 'cors',
				headers: { 
					'Content-Type': "text/plain",
				}, 
				body: JSON.stringify({
					body: this.editor.getValue()
				}),
			})



			let swtch = await fetch('http://192.168.4.1:6500/systemctl/switch', {
				method: 'post',
				credentials: 'same-origin',
				mode: 'cors',
				headers: { 
					'Content-Type': "text/plain",
				}, 
				body: JSON.stringify({
					state: 'restart'
				}),
			})

			let message = (await yml.json()).message; 
				message = message.substring(0, message.indexOf('!'));
				message += ' and ' + (await swtch.json()).message;

			this.response = {
				message: message 
			}; 
		}
	}
}

const SensorLogs = { 
	template: '#journalctl-logs-template',
	data: function() {
		return {
			logs: '',
			windowHeight: 0,
		}
	},
	mounted: async function() {
		let ws = new WebSocket('ws://192.168.4.1:6550/journalctl');
		// const reader = new FileReader();
		let logs = sessionStorage.getItem('sensorproxy-logs') ? sessionStorage.getItem('sensorproxy-logs') : '';
		this.logs = logs.trim(); 

		vm = this;

		vm.windowHeight = window.innerHeight-50; 
		
		ws.addEventListener('open', (evt) => console.log('WS: [OPEN]',evt))
		ws.addEventListener('error', (err) => console.log('WS: [ERROR]',err))
		ws.addEventListener('message', (evt) => vm.logs += evt.data+'\n')
		ws.addEventListener('close', (evt) => console.log('WS: [CLOSE]', evt))

		window.onbeforeunload = function() {
			ws.close();
			sessionStorage.setItem('sensorproxy-logs', vm.logs);
		};

		window.addEventListener('resize', (evt) => {
			vm.windowHeight = evt.target.innerHeight-50;
			console.log(evt.target);
		})
	},
	methods: {
		sensorState: async function(state) {
			let res = await fetch('http://192.168.4.1:6500/systemctl/switch', {
				method: 'post',
				credentials: 'same-origin',
				mode: 'cors',
				headers: { 
					'Content-Type': "text/plain",
				}, 
				body: JSON.stringify({
					state: state
				}),
			})
		},
		clearLogs: function() {
			this.logs = '';
			sessionStorage.setItem('sensorproxy-logs', '');
		}
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
		{ path: '/', component: YamlModifier },
		{ path: '/logs', component: SensorLogs }
	]
})

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
