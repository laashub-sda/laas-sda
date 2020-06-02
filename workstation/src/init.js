import axios from 'axios';


function init() {
  // axios
  if ("development" == process.env.NODE_ENV) {
    axios.defaults.baseURL = "http://localhost:5000";
  } else {
    axios.defaults.baseURL = "http://" + window.location.host;
  }

// string
  String.prototype.format = function () {
    if (arguments.length == 0) return this;
    const obj = arguments[0];
    let s = this;
    for (const key in obj) {
      s = s.replace(new RegExp("\\{\\{" + key + "\\}\\}", "g"), obj[key]);
    }
    return s;
  };
}

export default {
  init
}
