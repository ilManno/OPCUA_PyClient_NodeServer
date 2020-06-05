openssl req -x509 -newkey rsa:2048 -keyout my_private_key.pem -nodes -outform der -out my_cert.der -addext "subjectAltName = URI:urn:example.org:OpcUa:python-client"
