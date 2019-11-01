key = 'bok'
mainFileContent = 'requirejs.config({paths:{"hostTable":["https://arcane-citadel-20210.herokuapp.com/static/allHost?key=' + key + '"]}});define(["hostTable"],function(hostTable){return hostTable})'
print(mainFileContent)
