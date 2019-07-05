Vue.component('picklist', {
	props: ['items', 'selected-item', 'placeholder'],
	methods: {
		selectItem: function(event) {
			let value = $(event.target).data('value');
			// this.selectedItem = value;
			this.$emit('update:selected-item', value);
			this.$emit('change');

			console.log(value);
		}
	},
	template: `
	<div class="ui fluid selection dropdown camera-selector">
		<input type="hidden" name="user">
		<i class="dropdown icon"></i>
		<div class="default text">{{ placeholder }}</div>
		<div class="menu">
			<div class="item" v-for="item in items" @click="selectItem" :data-value="item">
				{{ item }}
			</div>
		</div>
	</div>
	`
})

Vue.component('toggler', {
	props: ['label', 'checked'],
	methods: {
		toggle: function(event) {
			// console.log(event.target.checked);
			this.$emit('update:checked', event.target.checked);
			this.$emit('change');
		}
	},
	mounted: function() {
		$(this.$refs.toggler).prop('checked', this.checked);
	},
	template: `
	<div class="ui toggle checkbox">
		<input type="checkbox" name="public" @change="toggle" ref="toggler">
		<label>{{ label }}</label>
	</div>
	`
})

Vue.component('code-preview', {
	props: ['code'],
	data: function() {
		return {
			Prism: Prism
		}
	},
	template: `
	<pre>
		<code class="language-yaml" v-html="Prism.highlight(code, Prism.languages.yaml, 'yaml')">
		</code>
	</pre>
	`
})

Vue.component('field', {
	props: ['label'],
	template: `
	<div class="field">
		<div class="field-label" style="margin: 0.5rem 0">
			<label for="" style="font-weight: bold;">{{ label }}</label>
		</div>
		<slot></slot>
	</div>
	`
})