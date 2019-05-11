
const app = new Vue({
  el: "#app1",
  data: {
    nodes: {}
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
    computed: {
        grid_names: function () {
            cols = 3;
            node_names = Object.keys(this.nodes);
            rows = Math.ceil(node_names.length/cols);
            grid = [];
            for (var i=0; i<rows; i++){
                row = node_names.slice(i*cols, i*cols+cols);
                grid.push(row)
            }
            return grid;
        },
        node_names: function () {
            return Object.keys(this.nodes)
        }
    },
  template: `
    <div class="container-fluid">
      <div v-for="row in grid_names" class="row">
          <div v-for="node_name in row" class="col-sm-4">
              <div class="panel panel-primary">
                <div class="panel-heading">
                    {{node_name}}
                    <button v-if="nodes[node_name].running" class="pull-right close" type="button" v-on:click="on_click('_kill', node_name)">
                        &times;
                    </button>
                    <span v-else class="pull-right badge">
                        Shutting Down ...
                    </span>
                </div>
                <div class="panel-body">
                  <div v-for="(ui_element, ui_element_name) in nodes[node_name]">
                    <button v-if="ui_element.type=='Button'" v-bind:disabled="!nodes[node_name].running" v-bind:class="ui_element.button_class" type="button" v-on:click="on_click(ui_element.topic, ui_element.data)">
                        {{ui_element_name}}
                    </button>
                  </div>  
                </div>
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

