<template>
	<ul class="nav">
		<li class="nav-profile">
			<a href="javascript:;" v-on:click="expand()">
				<div class="cover with-shadow"></div>
				<div class="image image-icon bg-black text-grey-darker">
					<i class="fa fa-user"></i>
				</div>
				<div class="info">
					<b class="caret pull-right"></b>
					张三
					<small>开发人员</small>
				</div>
			</a>
		</li>
		<li>
			<ul class="nav nav-profile" v-bind:class="{ 'd-block': this.stat == 'expand', 'd-none': this.stat == 'collapse' }">
				<li><a href="javascript:;"><i class="fa fa-cog"></i> 设置</a></li>
			</ul>
		</li>
	</ul>
</template>

<script>

export default {
	name: 'SidebarNavProfile',
	data() {
		return {
			stat: ''
		}
	},
	methods: {
		expand: function() {
			this.stat = (this.stat == 'expand') ? 'collapse' : 'expand'
		}
  }
}
</script>
