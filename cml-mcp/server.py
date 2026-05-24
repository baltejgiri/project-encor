import os
import json
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
from virl2_client import ClientLibrary

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

CML_HOST     = os.environ["CML_HOST"]
CML_USERNAME = os.environ["CML_USERNAME"]
CML_PASSWORD = os.environ["CML_PASSWORD"]

mcp = FastMCP("cml")


def _client() -> ClientLibrary:
    return ClientLibrary(
        f"https://{CML_HOST}",
        CML_USERNAME,
        CML_PASSWORD,
        ssl_verify=False,
    )


@mcp.tool()
def list_labs() -> str:
    """List all labs on the CML server with their ID, title, and state."""
    cl = _client()
    labs = cl.all_labs()
    result = [
        {"id": lab.id, "title": lab.title, "state": lab.state()}
        for lab in labs
    ]
    return json.dumps(result, indent=2)


@mcp.tool()
def create_lab(title: str, topology_yaml: str) -> str:
    """
    Create a new CML lab from a YAML topology string.

    Args:
        title: Human-readable lab name (e.g. 'Ch 1 – Packet Forwarding').
        topology_yaml: Full CML topology YAML defining nodes, interfaces, and links.

    Returns:
        JSON with the new lab's id and title.
    """
    cl = _client()
    lab = cl.import_lab(topology_yaml, title=title)
    return json.dumps({"id": lab.id, "title": lab.title, "state": lab.state()})


@mcp.tool()
def get_lab(lab_id: str) -> str:
    """
    Get details for a lab including its nodes and their states.

    Args:
        lab_id: The CML lab ID returned by list_labs or create_lab.
    """
    cl = _client()
    lab = cl.join_existing_lab(lab_id)
    nodes = [
        {
            "id": node.id,
            "label": node.label,
            "node_definition": node.node_definition,
            "state": node.state,
        }
        for node in lab.nodes()
    ]
    return json.dumps({"id": lab.id, "title": lab.title, "state": lab.state(), "nodes": nodes}, indent=2)


@mcp.tool()
def start_lab(lab_id: str) -> str:
    """
    Start all nodes in a lab.

    Args:
        lab_id: The CML lab ID.
    """
    cl = _client()
    lab = cl.join_existing_lab(lab_id)
    lab.start()
    return json.dumps({"id": lab.id, "title": lab.title, "state": lab.state()})


@mcp.tool()
def stop_lab(lab_id: str) -> str:
    """
    Stop all nodes in a lab.

    Args:
        lab_id: The CML lab ID.
    """
    cl = _client()
    lab = cl.join_existing_lab(lab_id)
    lab.stop()
    return json.dumps({"id": lab.id, "title": lab.title, "state": lab.state()})


@mcp.tool()
def delete_lab(lab_id: str) -> str:
    """
    Stop and delete a lab permanently.

    Args:
        lab_id: The CML lab ID.
    """
    cl = _client()
    lab = cl.join_existing_lab(lab_id)
    lab.stop()
    lab.wipe()
    cl.remove_lab(lab_id)
    return json.dumps({"deleted": lab_id})


@mcp.tool()
def get_lab_topology(lab_id: str) -> str:
    """
    Export the YAML topology of an existing lab.

    Args:
        lab_id: The CML lab ID.
    """
    cl = _client()
    lab = cl.join_existing_lab(lab_id)
    return lab.download()


if __name__ == "__main__":
    mcp.run()
