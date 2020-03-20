var e = /d{1,4}|M{1,4}|YY(?:YY)?|S{1,3}|Do|ZZ|Z|([HhMsDm])\1?|[aA]|"[^"]*"|'[^']*'/g,
    t = "[^\\s]+",
    r = /\[([^]*?)\]/gm;function n(e, t) {
  for (var r = [], n = 0, o = e.length; n < o; n++) r.push(e[n].substr(0, t));return r;
}var o = function (e) {
  return function (t, r) {
    var n = r[e].map(function (e) {
      return e.toLowerCase();
    }).indexOf(t.toLowerCase());return n > -1 ? n : null;
  };
};function a(e) {
  for (var t = [], r = 1; r < arguments.length; r++) t[r - 1] = arguments[r];for (var n = 0, o = t; n < o.length; n++) {
    var a = o[n];for (var i in a) e[i] = a[i];
  }return e;
}var i = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
    u = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
    s = n(u, 3),
    c = { dayNamesShort: n(i, 3), dayNames: i, monthNamesShort: s, monthNames: u, amPm: ["am", "pm"], DoFn: function (e) {
    return e + ["th", "st", "nd", "rd"][e % 10 > 3 ? 0 : (e - e % 10 != 10 ? 1 : 0) * e % 10];
  } },
    l = a({}, c),
    d = function (e, t) {
  for (void 0 === t && (t = 2), e = String(e); e.length < t;) e = "0" + e;return e;
},
    m = { D: function (e) {
    return String(e.getDate());
  }, DD: function (e) {
    return d(e.getDate());
  }, Do: function (e, t) {
    return t.DoFn(e.getDate());
  }, d: function (e) {
    return String(e.getDay());
  }, dd: function (e) {
    return d(e.getDay());
  }, ddd: function (e, t) {
    return t.dayNamesShort[e.getDay()];
  }, dddd: function (e, t) {
    return t.dayNames[e.getDay()];
  }, M: function (e) {
    return String(e.getMonth() + 1);
  }, MM: function (e) {
    return d(e.getMonth() + 1);
  }, MMM: function (e, t) {
    return t.monthNamesShort[e.getMonth()];
  }, MMMM: function (e, t) {
    return t.monthNames[e.getMonth()];
  }, YY: function (e) {
    return d(String(e.getFullYear()), 4).substr(2);
  }, YYYY: function (e) {
    return d(e.getFullYear(), 4);
  }, h: function (e) {
    return String(e.getHours() % 12 || 12);
  }, hh: function (e) {
    return d(e.getHours() % 12 || 12);
  }, H: function (e) {
    return String(e.getHours());
  }, HH: function (e) {
    return d(e.getHours());
  }, m: function (e) {
    return String(e.getMinutes());
  }, mm: function (e) {
    return d(e.getMinutes());
  }, s: function (e) {
    return String(e.getSeconds());
  }, ss: function (e) {
    return d(e.getSeconds());
  }, S: function (e) {
    return String(Math.round(e.getMilliseconds() / 100));
  }, SS: function (e) {
    return d(Math.round(e.getMilliseconds() / 10), 2);
  }, SSS: function (e) {
    return d(e.getMilliseconds(), 3);
  }, a: function (e, t) {
    return e.getHours() < 12 ? t.amPm[0] : t.amPm[1];
  }, A: function (e, t) {
    return e.getHours() < 12 ? t.amPm[0].toUpperCase() : t.amPm[1].toUpperCase();
  }, ZZ: function (e) {
    var t = e.getTimezoneOffset();return (t > 0 ? "-" : "+") + d(100 * Math.floor(Math.abs(t) / 60) + Math.abs(t) % 60, 4);
  }, Z: function (e) {
    var t = e.getTimezoneOffset();return (t > 0 ? "-" : "+") + d(Math.floor(Math.abs(t) / 60), 2) + ":" + d(Math.abs(t) % 60, 2);
  } },
    f = function (e) {
  return +e - 1;
},
    g = [null, "[1-9]\\d?"],
    h = [null, t],
    p = ["isPm", t, function (e, t) {
  var r = e.toLowerCase();return r === t.amPm[0] ? 0 : r === t.amPm[1] ? 1 : null;
}],
    y = ["timezoneOffset", "[^\\s]*?[\\+\\-]\\d\\d:?\\d\\d|[^\\s]*?Z?", function (e) {
  var t = (e + "").match(/([+-]|\d\d)/gi);if (t) {
    var r = 60 * +t[1] + parseInt(t[2], 10);return "+" === t[0] ? r : -r;
  }return 0;
}],
    v = (o("monthNamesShort"), o("monthNames"), { default: "ddd MMM DD YYYY HH:mm:ss", shortDate: "M/D/YY", mediumDate: "MMM D, YYYY", longDate: "MMMM D, YYYY", fullDate: "dddd, MMMM D, YYYY", isoDate: "YYYY-MM-DD", isoDateTime: "YYYY-MM-DDTHH:mm:ssZ", shortTime: "HH:mm", mediumTime: "HH:mm:ss", longTime: "HH:mm:ss.SSS" });var M = function (t, n, o) {
  if (void 0 === n && (n = v.default), void 0 === o && (o = {}), "number" == typeof t && (t = new Date(t)), "[object Date]" !== Object.prototype.toString.call(t) || isNaN(t.getTime())) throw new Error("Invalid Date pass to format");var i = [];n = (n = v[n] || n).replace(r, function (e, t) {
    return i.push(t), "@@@";
  });var u = a(a({}, l), o);return (n = n.replace(e, function (e) {
    return m[e](t, u);
  })).replace(/@@@/g, function () {
    return i.shift();
  });
},
    w = (function () {
  try {
    new Date().toLocaleDateString("i");
  } catch (e) {
    return "RangeError" === e.name;
  }
}(), function () {
  try {
    new Date().toLocaleString("i");
  } catch (e) {
    return "RangeError" === e.name;
  }
}(), function () {
  try {
    new Date().toLocaleTimeString("i");
  } catch (e) {
    return "RangeError" === e.name;
  }
}(), function (e, t, r, n) {
  n = n || {}, r = null == r ? {} : r;var o = new Event(t, { bubbles: void 0 === n.bubbles || n.bubbles, cancelable: Boolean(n.cancelable), composed: void 0 === n.composed || n.composed });return o.detail = r, e.dispatchEvent(o), o;
}),
    S = new Set(["call-service", "divider", "section", "weblink", "cast", "select"]),
    b = { alert: "toggle", automation: "toggle", climate: "climate", cover: "cover", fan: "toggle", group: "group", input_boolean: "toggle", input_number: "input-number", input_select: "input-select", input_text: "input-text", light: "toggle", lock: "lock", media_player: "media-player", remote: "toggle", scene: "scene", script: "script", sensor: "sensor", timer: "timer", switch: "toggle", vacuum: "toggle", water_heater: "climate", input_datetime: "input-datetime" },
    D = (e, t) => {
  if (!e && !t.default) return t.card;let r = [];e && (r = e.slice(0)), t.default && (r = r.concat(t.default));let n = JSON.stringify(t.card);return r.forEach(e => {
    const t = Object.keys(e)[0],
          r = Object.values(e)[0],
          o = new RegExp(`\\[\\[${t}\\]\\]`, "gm");if ("number" == typeof r || "boolean" == typeof r) {
      const e = new RegExp(`"\\[\\[${t}\\]\\]"`, "gm");n = n.replace(e, r);
    }if ("object" == typeof r) {
      const e = new RegExp(`"\\[\\[${t}\\]\\]"`, "gm"),
            o = JSON.stringify(r);n = n.replace(e, o);
    } else n = n.replace(o, r);
  }), JSON.parse(n);
};let Y = window.cardHelpers;const H = new Promise(async e => {
  Y && e(), window.loadCardHelpers && (Y = await window.loadCardHelpers(), window.cardHelpers = Y, e());
});class _ extends HTMLElement {
  constructor() {
    super(), this.attachShadow({ mode: "open" });
  }set hass(e) {
    this._card && (this._card.hass = e);
  }setConfig(e) {
    if (!e.template) throw new Error("Missing template object in your config");const t = function () {
      var e = document.querySelector("home-assistant");if (e = (e = (e = (e = (e = (e = (e = (e = e && e.shadowRoot) && e.querySelector("home-assistant-main")) && e.shadowRoot) && e.querySelector("app-drawer-layout partial-panel-resolver")) && e.shadowRoot || e) && e.querySelector("ha-panel-lovelace")) && e.shadowRoot) && e.querySelector("hui-root")) {
        var t = e.lovelace;return t.current_view = e.___curView, t;
      }return null;
    }() || function () {
      let e = document.querySelector("hc-main");if (e = e && e.shadowRoot, e = e && e.querySelector("hc-lovelace"), e = e && e.shadowRoot, e = e && e.querySelector("hui-view"), e) {
        const t = e.lovelace;return t.current_view = e.___curView, t;
      }return null;
    }();if (!t.config && !t.config.decluttering_templates) throw new Error("The object decluttering_templates doesn't exist in your main lovelace config.");const r = t.config.decluttering_templates[e.template];if (!r || !r.card) throw new Error(`The template "${e.template}" doesn't exist in decluttering_templates`);const n = this.shadowRoot;for (; n && n.hasChildNodes();) n.removeChild(n.lastChild);const o = document.createElement("div");if (o.id = "root", n.appendChild(o), Y) {
      const t = Y.createCardElement(D(e.variables, r));return t.hass = this.hass, o.appendChild(t), this._card = t, t;
    }{
      const t = function (e, t) {
        void 0 === t && (t = !1);var r = function (e, t) {
          return n("hui-error-card", { type: "error", error: e, config: t });
        },
            n = function (e, t) {
          var n = window.document.createElement(e);try {
            n.setConfig(t);
          } catch (n) {
            return console.error(e, n), r(n.message, t);
          }return n;
        };if (!e || "object" != typeof e || !t && !e.type) return r("No type defined", e);var o = e.type;if (o && o.startsWith("custom:")) o = o.substr("custom:".length);else if (t) {
          if (S.has(o)) o = "hui-" + o + "-row";else {
            if (!e.entity) return r("Invalid config given.", e);var a = e.entity.split(".", 1)[0];o = "hui-" + (b[a] || "text") + "-entity-row";
          }
        } else o = "hui-" + o + "-card";if (customElements.get(o)) return n(o, e);var i = r("Custom element doesn't exist: " + e.type + ".", e);i.style.display = "None";var u = setTimeout(function () {
          i.style.display = "";
        }, 2e3);return customElements.whenDefined(e.type).then(function () {
          clearTimeout(u), w(i, "ll-rebuild", {}, i);
        }), i;
      }(D(e.variables, r));return t.hass = this.hass, o.appendChild(t), this._card = t, H.then(() => {
        w(t, "ll-rebuild", {});
      }), t;
    }
  }getCardSize() {
    return "function" == typeof this._card.getCardSize ? this._card.getCardSize() : 1;
  }
}customElements.define("decluttering-card", _);
