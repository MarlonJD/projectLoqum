requirejs.config({
	paths: {
	  'hostTable': ['https://arcane-citadel-20210.herokuapp.com/static/allHost']
	}
  });
  
  define(['hostTable'],function(hostTable){
	  return hostTable;
  });