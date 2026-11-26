function Span(el)
  local color = string.match(el.attributes.style or "", "color:%s*(%a+)")
  if color == "red" then el.attributes["custom-style"] = "SourceBlank" end
  if color == "blue" then el.attributes["custom-style"] = "SourceAnnotation" end
  return el
end
