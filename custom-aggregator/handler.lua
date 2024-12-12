local http = require "resty.http"
local cjson = require "cjson.safe"

local CustomAggregator = {
    VERSION = "1.0.0",
    PRIORITY = 10,
}

local function fetch_service_data(host, port, path, method, body)
  local httpc = http.new()
  local url = "http://" .. host .. ":" .. port .. (path or "")

  local body_str = body
  if type(body) == "table" then
      body_str = cjson.encode(body)
  end

  local res, err = httpc:request_uri(url, {
      method = method,
      body = body_str,
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

function CustomAggregator:access(config)
    local path = kong.request.get_path()

    local path_segments = {}
    for segment in path:gmatch("[^/]+") do
        table.insert(path_segments, segment)
    end

    if #path_segments < 3 then
        kong.response.exit(400, { error = "Invalid path format. Expected '/kong-gateway/{category}/reserve'." })
    end

    local category = path_segments[2]

    if not category then
        kong.response.exit(400, { error = "Category is required in the URL path" })
    end

    local services = {
        grand_oak = { host = "grand-oak", port = "8080", path = "/" .. category .. "/reserve" },
        pine_valley = { host = "pine-valley", port = "8080", path = "/api/v1/categories/" .. category .. "/reserve" },
        willow_gardens = { host = "willow-gardens", port = "8080", path = "/" .. category .. "/reserve" },
    }

    local method = kong.request.get_method()
    local body = kong.request.get_body()

    local responses = {}
    for name, service in pairs(services) do
        responses[name] = fetch_service_data(service.host, service.port, service.path, method, body)
    end

    kong.response.exit(200, responses)
end

return CustomAggregator
