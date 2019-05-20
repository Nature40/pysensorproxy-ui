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
		camera: { value: '' }
	},
	items: ['Camera 1','Camera 2','Camera 3','Camera 4']
};

const app = new Vue({
	router,
	el: '#app',
	data: state,
	mounted: function() {
		this.generateScript();
	},
	methods: {
		generateScript: function() {
			// console.log(
			// 	'generateScript',this.selected.camera.value);
			let gs = ''+
			SensorScript.section.cam(this.selected.camera.value)+
			SensorScript.section.log()+
			SensorScript.section.wifi()+
			SensorScript.section.lift();

			this.sensor_script = gs; 
		}
	}
})

$(document).ready(() => {
	$('#app .camera-selector').dropdown();
})