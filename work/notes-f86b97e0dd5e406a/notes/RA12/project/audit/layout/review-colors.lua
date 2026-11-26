function BlockQuote(el)
  local r={pandoc.RawBlock("latex","{\\color{blue}")}
  for _,b in ipairs(el.content) do table.insert(r,b) end
  table.insert(r,pandoc.RawBlock("latex","}"))
  return r
end
function Span(el)
  local style=el.attributes.style or ""
  local color=string.match(style,"color:%s*(%a+)")
  if color then
    local r={pandoc.RawInline("latex","{\\color{"..color.."}")}
    for _,x in ipairs(el.content) do table.insert(r,x) end
    table.insert(r,pandoc.RawInline("latex","}"))
    return r
  end
end
