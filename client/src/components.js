Vue.component('picklist', {
	props: ['items', 'selected-item'],
	methods: {
		selectItem: function(event) {
			this.selectedItem.value = $(event.target).data('value');
			this.$emit('change');
		}
	},
	template: `
	<div class="ui fluid selection dropdown camera-selector">
		<input type="hidden" name="user">
		<i class="dropdown icon"></i>
		<div class="default text">Select Camera</div>
		<div class="menu">
			<div class="item" v-for="item in items" @click="selectItem" :data-value="item">
				{{ item }}
			</div>
		</div>
	</div>
	`
})

Vue.component('toggler', {
	props: ['label'],
	template: `
	<div class="ui toggle checkbox">
		<input type="checkbox" name="public">
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