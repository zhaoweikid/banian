<template>
	<!-- begin login -->
	<div class="login bg-black animated fadeInDown">
		<!-- begin brand -->
		<div class="login-header">
			<div class="brand">
				<span class="logo"></span> <b>Banian</b>
				<small>workshop for development</small>
			</div>
			<div class="icon">
				<i class="fa fa-lock"></i>
			</div>
		</div>
		<!-- end brand -->
		<!-- begin login-content -->
		<div class="login-content">
			<form v-on:submit="checkForm" method="POST" class="margin-bottom-0">
				<div class="form-group m-b-20">
					<input type="text" class="form-control form-control-lg inverse-mode" placeholder="User/Mobile/Email" required />
				</div>
				<div class="form-group m-b-20">
					<input type="password" class="form-control form-control-lg inverse-mode" placeholder="Password" required />
				</div>
				<div class="checkbox checkbox-css m-b-20">
					<input type="checkbox" id="remember_checkbox" /> 
					<label for="remember_checkbox">
					记住我
					</label>
				</div>
				<div class="login-buttons">
					<button type="submit" class="btn btn-success btn-block btn-lg"> 登 录 </button>
				</div>
			</form>
		</div>
		<!-- end login-content -->
	</div>
	<!-- end login -->
</template>

<script>
import PageOptions from '../config/PageOptions.vue'

export default {
	created() {
		PageOptions.pageEmpty = true;
	},
	beforeRouteLeave (to, from, next) {
		PageOptions.pageEmpty = false;
		next();
	},
	methods: {
		checkForm: function(e) {
			e.preventDefault();
			this.$router.push({ path: '/ui/v1/login'})
		}
	}
}
</script>
