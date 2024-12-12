local BasePlugin = require "kong.plugins.base_plugin"
local http = require "resty.http"

local CustomAggregator = BasePlugin:extend()

function CustomAggregator:new()
    CustomAggregator.super.new(self, "custom-aggregator")
end

function CustomAggregator:access(config)
    CustomAggregator.super.access(self)

    -- Create an HTTP client
    local httpc = http.new()

    -- Function to fetch data from a service
    local function fetch_service_data(service_url)
        local res, err = httpc:request_uri(service_url, { method = "GET" })
        if not res then
            kong.log.err("Failed to fetch data from ", service_url, ": ", err)
            return nil
        end
        return res.body
    end

    -- Fetch responses from all three services
    local grand_oak_data = fetch_service_data("http://grand-oak:8080/endpoint") or "{}"
    local pine_valley_data = fetch_service_data("http://pine-valley:8080/endpoint") or "{}"
    local willow_gardens_data = fetch_service_data("http://willow-gardens:8080/endpoint") or "{}"

    -- Aggregate the responses
    local aggregated_response = {
        grand_oak = grand_oak_data,
        pine_valley = pine_valley_data,
        willow_gardens = willow_gardens_data
    }

    -- Send the aggregated response
    return kong.response.exit(200, aggregated_response)
end

return CustomAggregator
