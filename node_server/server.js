let os = require("os");

let opcua = require("node-opcua");

let server = new opcua.OPCUAServer({
    port: 4334,
    resourcePath: "/UA/RaspServer",
    buildInfo: {
        productName: "RaspUAServer1",
        buildNumber: "1",
        buildDate: new Date()
    }
});

server.initialize(() => {
    console.log("OPC UA Server initialized.");

    function build_my_address_space(server) {
        const addressSpace = server.engine.addressSpace;
        const namespace = addressSpace.getOwnNamespace();

        //declare a new object
        let device = namespace.addObject({
            organizedBy: addressSpace.rootFolder.objects,
            browseName: "MyDevice"
        });

    }

    build_my_address_space(server);
    console.log("Address space initialized.");

    server.start(() => {
        console.log(`Server is now listening port ${server.endpoints[0].port}... (press CTRL+C to stop)`);
        let endpointUrl = server.endpoints[0].endpointDescriptions()[0].endpointUrl;
        console.log("The primary server endpoint url is ", endpointUrl);
    });
});

process.on('SIGINT', function () {
    util.freeResources();
    process.exit(0);
});
