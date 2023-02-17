$listener = New-Object System.Net.HttpListener
$listener.Prefixes.Add("http://localhost:8080/")
$listener.Start()

while ($true) {
    $context = $listener.GetContext()
    $request = $context.Request
    $response = $context.Response

    if ($request.HttpMethod -eq "POST") {
        $file = $request.Files["file"]
        
        # process the file content here
        $responseString = '{"result": "processed"}'
        $responseContent = [System.Text.Encoding]::UTF8.GetBytes($responseString)
        $response.ContentLength64 = $responseContent.Length
        $response.OutputStream.Write($responseContent, 0, $responseContent.Length)
    }
}

$listener.Stop()
