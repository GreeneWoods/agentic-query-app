# agentic-query-app

## Quickstart

```bash
export OPENAI_API_KEY="your_openai_api_key"
docker compose run --rm --service-ports --name leads_agent_run -it agent
```
This should result in the api, and mcp server spinning up. It should also spin up
an agent that you can interact with via the terminal.

The first time you interact with the agent, and it makes a call to the mcp -> api -> db it will
take an extra moment to spin up the database.  Please forgive this additional latency. Once that's
complete it should be a bit smoother.

A few suggested prompts include
1. a sanity check: "ping" -> "pong"
2. a memory check: "my favorite fruit is an apple" -> response -> "what's my favorite fruit?" -> "apple"
3. a connectivity check: "please find me my high priority leads in new york" -> "a list of new york leads"

From there we are off to the races.  I also included a minimal event_stream_handler so that 
you can see the agent's tools in action.  I find that it helps to understand inputs/outputs.

When you're complete, kill the container with `CTRL+C` and then be sure to run `docker compose down` 
to decompose everything that was spun up.


The initial startup process takes a few minutes, so while we have some time to let the infra spin up,
let's talk through the project structure.

## Overview

There are 4 layers to the project and they relate to one another as follows:

Agent <> MCP <> API <> DB

I built them as separate applications to reflect what the system would look like as a 
suite of microservices. In a production system, these would be deployed and scaled separately.

The distributed architecture allows for highly scalable, maintainable, and flexible systems.

Ultimately it fosters reusability.  This allows for us to make components that can support 
emergent systems on the fly.  We can adapt to needs as they arise.  New systems can be added
on without having to re-architect the entire system as a whole.

## Alternative Setup with Extended Visibility

My quickstart is quick, but it also hides a bunch of the moving parts from the user.
If you'd like to get a feel for what's going on under the hood, follow these steps:

#### In one terminal start the api and mcp
```bash
docker compose up --build api mcp
```

#### In another terminal start the agent
```bash
export OPENAI_API_KEY="your_openai_api_key"
docker compose run --rm --service-ports --name leads_agent_run -it agent
```

Now you will be able to see the interactions across the network as they occur.

As before when complete kill the container with `CTRL+C` and then be sure to run `docker compose down`.

## Bare Metal Python Setup

I have also included README's in each of the subdirectories that go into more detail.  They 
will guide for step-by-step setup at the pythonic level and will circumvent docker altogether.

I would recommend spinning up the api first, then the mcp, and finally the agent.  You will need
three separate terminals for this setup.

## Notes

I hope these steps serve you well.  I made this README using Ubuntu, while I believe these commands
should transfer, you may need to make some adjustments for your OS.  I also used OpenAI's api for this solution,
but I'm confident it can be altered to use other LLM providers without any additional effort.

## Troubleshooting

If for whatever reason the db doesn't spin up properly please follow these steps:
1. follow the instructions in the leads_api/README.md.
2. uncomment ./leads_api/db.py:7
3. start the api
4. stop the api
5. comment out ./leads_api/db.py:7
6. restart the api
7. open another terminal
8. activate the api virtual environment
9. navigate to the root folder
10. `python pipeline.py`

The process is idempotent, so it should be safe to run multiple times, or with incomplete
data.