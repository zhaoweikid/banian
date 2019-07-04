<template>
	<!-- begin navbar-collapse -->
	<div class="collapse navbar-collapse pull-left" id="top-navbar" v-bind:class="{ 'd-block': pageOptions.pageMobileMegaMenu }">
		<ul class="nav navbar-nav">
			
			<li class="dropdown">
				<a href="javascript:;">
					<i class="fa fa-gem fa-fw"></i> 产品 
				</a>
			</li>

			<li class="dropdown">
				<a href="javascript:;">
				<i class="fa fa-database fa-fw"></i> 项目
				</a>
			</li>

			<li class="dropdown">
				<a href="javascript:;">
				<i class="fa fa-train fa-fw"></i> 迭代
				</a>
			</li>



			<li class="dropdown">
				<a href="javascript:;">
				<i class="fa fa-users fa-fw"></i> 团队
				</a>
			</li>


			<li class="dropdown">
				<a href="javascript:;">
					<i class="fa fa-paperclip a-fw"></i> 标签
				</a>
			</li>

		</ul>
	</div>
	<!-- end navbar-collapse -->
</template>

<script>
import PageOptions from '../../config/PageOptions.vue'

export default {
  name: 'HeaderMegaMenu',
  data() {
		return {
			pageOptions: PageOptions
		}
  }
}
</script>
