from app.utils import cfg, get_logger
from typing import Literal



from typing import Dict

log = get_logger(__file__)



def router_node(agent_state: Dict) -> Literal["", ""]:
    sentiment = agent_state.get("sentiment", "neutral")
    topics = agent_state("topic")

    log.info(f"Routing request with sentiment: {sentiment} and topics: {topics}")

    if "something" in topics:
        # todo - forward to answer node
        return "node name"

    if "something" in sentiment:
        # todo - forward to ens node
        return "node name"


    



    