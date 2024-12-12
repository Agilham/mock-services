local http = require "resty.http"
local cjson = require "cjson.safe"

local CustomAggregator = {
    VERSION = "1.0.0",
    PRIORITY = 10,
}

local function fetch_service_data(host, path, method, body)
    local httpc = http.new()
    local url = "http://" .. host .. (path or "")
    local res, err = httpc:request_uri(url, {
        method = method,
        body = body,
        headers = { ["Content-Type"] = "application/json" },
        keepalive = false,
    })
    if not res then
        kong.log.err("Failed to fetch data from ", url, ": ", err)
        return { error = err }
    end

    local parsed_body, parse_err = cjson.decode(res.body)
    if not parsed_body then
        kong.log.err("Failed to parse response from ", url, ": ", parse_err)
        return { error = "Invalid JSON response" }
    end

    return parsed_body
end

-- Access handler to manage incoming request
function CustomAggregator:access(config)
    local services = {
        grand_oak = { host = "grand-oak", path = "/reserve" },
        pine_valley = { host = "pine-valley", path = "/api/v1/categories/reserve" },
        willow_gardens = { host = "willow-gardens", path = "/reserve" },
    }

    local method = kong.request.get_method()
    local body = kong.request.get_body()

    local responses = {}
    for name, service in pairs(services) do
        responses[name] = fetch_service_data(service.host, service.path, method, body)
    end

    local aggregated_response = {
        grand_oak = responses.grand_oak,
        pine_valley = responses.pine_valley,
        willow_gardens = responses.willow_gardens,
    }

    kong.response.exit(200, cjson.encode(aggregated_response))
end

return CustomAggregator
