
const app = new Vue({
  el: "#app1",
  data: {
    nodes: []
  },
  methods: {

      on_click: function (topic, data) {
          console.log(topic);
          console.log(data);
          // let s = '/broadcast?topic=' + topic + "%data=" + data;
          // console.log(s);
          //$.post(s);
          var formData = new FormData();
          formData.append("topic", topic);
          formData.append("data", data);

          var request = new XMLHttpRequest();
            request.open("POST", "/broadcast");
            request.send(formData);

      }
  },
  template: `
    <div>
      <div v-for="(node, node_name) in nodes" class="panel panel-primary">
        <div class="panel-heading">{{node_name}}</div>
        <div class="panel-body">
          <div v-for="(ui_element, ui_element_name) in node">
            <button v-if="ui_element.type=='Button'" class="btn btn-default" type="button" v-on:click="on_click(ui_element.topic, ui_element.data)">
                {{ui_element_name}}
            </button>
          </div>  
        </div>
      </div>
    </div>
  `
});

var server = new EventSource('/state_stream');
server.onmessage = CostumePy_update;

function CostumePy_update(response) {
    var state = JSON.parse(response.data);
    console.log("updating state");
    console.log(state);
    app.nodes = state;
}

