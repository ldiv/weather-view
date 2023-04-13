
const app = Vue.createApp({
    delimiters: ['[[', ']]'],  // to avoid collision with jinja
    data() {
        return {
            search_input: "",
            filter: {
                "content-type": {
                    "class_selected": true,
                    "q_and_a_selected": true,
                    "meditation_selected": true,
                }
            },
            query: {},
            results: [],
            summary: {},
            active_tab: 0
        }
    },
    methods: {
        search() {
            let app = this
            app.query["zip"] = app.search_input
            axios.post('/report', app.query)
                .then(function (response) {
                    console.log("RESPONSE", response);
                    app.results.push(processResults(response.data))
                    app.summary = computeSummary(app.results[0]["hourly"])
                    console.log("SUMMARY", app.summary);
                })
                .catch(function (error) {
                    console.log("Something went wrong with API request", error);
                })
        },
        setActiveTab(tab_id) {
            this.active_tab = tab_id
        }

    },
    computed: {},
    watch: {}
}).mount('#app')


const processResults = function (response) {
    return JSON.parse(response);
}


const computeSummary = function (hourly_detail) {
    let summary = {}
    let previous_day
    for (let i=0; i<hourly_detail["time"].length; i++) {
        let time = hourly_detail["time"][i]
        let temp = hourly_detail["temperature_2m"][i]
        let day = time.split("T")[0]

        if (day in summary) {
            summary[day]["temp"].push(parseFloat(temp))
        }
        else {
            if (previous_day) {
                summary[previous_day]["temp_high"] = Math.max(...summary[previous_day]["temp"])
                summary[previous_day]["temp_low"] = Math.min(...summary[previous_day]["temp"])
            }
            summary[day] = {}
            summary[day]["temp"] = [parseFloat(temp)]
            previous_day = day
        }
    }
    // Add summary to last day
    summary[previous_day]["temp_high"] = Math.max(...summary[previous_day]["temp"])
    summary[previous_day]["temp_low"] = Math.min(...summary[previous_day]["temp"])

    return summary
}
