<! DOCTYPE html>
<html>
<body>
    <form action="" method="post" enctype="multipart/form-data">
        <input type="file" name="fileToUpload" id="fileToUpload">
        <input type="submit" value="Upload UWWTD reporting file" name="submit">
    </form>
    <br/>
</body>





<?php

if(isset($_POST["submit"])) {
    if (isXML($_FILES["fileToUpload"]["tmp_name"])) {
        $wps_request = encapsulateXmlInWps($_FILES["fileToUpload"]["tmp_name"]);
        $results     = sendRequesToWps($wps_request);
        echo "<div><textarea rows='50' cols='200'>".html_entity_decode($results)."</textarea></div>";
    }
    else {
        echo "Incorrect XML file";
    }
}

function isXML($url)
{
    libxml_use_internal_errors(false);
    $doc = new DOMDocument('1.0', 'utf-8'); 
    $doc->loadXML(file_get_contents($url));

    $errors = libxml_get_errors();
    if (empty($errors)) {
        return true;
    }
    return false;
}

function encapsulateXmlInWps($file)
{
    $xml_content = file_get_contents($file);
    $xml_content = str_replace('<?xml version="1.0" encoding="UTF-8"?>', '', $xml_content);
    $xml_content = str_replace('<!--?xml version="1.0" encoding="UTF-8"?-->','', $xml_content);


    return
        <<<EOD
<wps:Execute service="WPS" version="1.0.0" xmlns:wps="http://www.opengis.net/wps/1.0.0"
    xmlns:ows="http://www.opengis.net/ows/1.1" xmlns:xlink="http://www.w3.org/1999/xlink"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://www.opengis.net/wps/1.0.0 http://schemas.opengis.net/wps/1.0.0/wpsExecute_request.xsd">
    <ows:Identifier>UWWTDParser</ows:Identifier>
    <wps:DataInputs>
        <wps:Input>
            <ows:Identifier>uwwtd_data</ows:Identifier>
            <wps:Data>
                <wps:ComplexData mimeType="application/xml">
                $xml_content
                </wps:ComplexData>
            </wps:Data>
        </wps:Input>
    </wps:DataInputs>
</wps:Execute>
EOD;
}

function sendRequesToWps($xml)
{
    $url = 'http://map7nux.rnde.tm.fr/siifparser/wps';

    // initialise the curl request
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_HTTPHEADER, array('Content-Type: text/xml'));
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, $xml);
    $result = curl_exec($ch);
    curl_close($ch);
    return $result;
}

?>