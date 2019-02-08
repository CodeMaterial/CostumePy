var checked_knobs = []


$(document).ready(function() {
    var server = new EventSource('/state_stream');
    server.onmessage = CostumePy_update;

});

function CostumePy_update(response){
    var state = JSON.parse(response.data);

const app = new Vue({
  el: "#app1",
  data: {
    nodes: [
    {
      name: "Node Name",
      state_vars: {"State variable":"state", "State variable 2":"state 2", "State variable 3":"state 3"},
      ui_elements: [
          {"name":"something button",   "type":"button", "topic": "topic name",    "data":true},
          {"name":"something button 2", "type":"button", "topic": "topic name 2",  "data":false},
          {"name":"something slider",   "type":"slider", "topic": "slider topic",  "min":1,  "max":10, "val":5},
          {"name":"something slider 2", "type":"slider", "topic": "slider topic 2","min":10, "max":100, "val":10}
      ]
    },
    {
      name: "Node Name 2",
      state_vars: {"State variable":"state", "State variable 2":"state 2", "State variable 3":"state 3"},
    }]
  },
    updated() {
      $('.dial').each(function(index, knob){
	console.log($(knob));
	if(!checked_knobs.includes($(knob).attr('id'))){
		console.log("new knob");
		$(knob).knob({'change' : nob_change, 'knob_id' : $(knob).attr('id')});
		checked_knobs.push($(knob).attr('id'));
	}
        
      });
    },



  template: `
    <div>
      <div v-for="node in nodes" class="panel panel-primary">
        <div class="panel-heading">name: {{node.name}}</div>
        <div class="panel-body">
          <ul><li v-for="(state, var_name) in node.state_vars">
            {{var_name}}:{{state}}
          </li></ul>
          <div v-for="ui_element in node.ui_elements">
            <button v-if="ui_element.type=='button'" class="btn btn-default" type="button">
                {{ui_element.name}}
            </button>
            <div v-if="ui_element.type=='slider'">
                {{ui_element.name}}  
                <input v-bind:id="ui_element.name" v-bind:value="ui_element.val" type="text" class="dial" data-cursor=true>
1
            </div>
          </div>  
        </div>
      </div>
    </div>
  `
});


function nob_change(v, id){
  console.log(id);
  console.log(v);
}

