async function main (event, context) {
    const { CosmosClient } = require("@azure/cosmos");
    const endpoint = process.env.documentdb_host_endpoint;
    const key = process.env.documentdb_master_key;
    const client = new CosmosClient({ endpoint, key });
    const databaseId = process.env.databaseName;
    const containerId = "Demo";
    var today = new Date();
    var time = today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds();
    const itemBody = { id: "update", time: time };
    await client.database(databaseId).container(containerId).item(itemBody.id).replace(itemBody);
    event.extensions.response.status(200).send(JSON.stringify(itemBody));
}

module.exports.main = main;