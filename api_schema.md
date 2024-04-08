# Routes

## POST /search

### Request payload
```
{
  target?: Str:"value",
  type: Enum:["Channel", "User"],
  timeframe?: Num:<0
}
```

### Response payload
```
{
    results: ChannelEntity[]
}
```
