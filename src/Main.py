from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from netmiko import ConnectHandler, NetmikoTimeoutException, NetmikoAuthenticationException
from typing import Optional
import FSMfun as FSM
app = FastAPI(title="FastAPI + Netmiko API", description="Run network commands via REST API", version="1.0.0")

# Request model for device connection
class DeviceCommand(BaseModel):
    device_type: str
    host: str
    username: str
    password: str
    secret: Optional[str]
    command: str
class Devicespush(BaseModel):
    device_type: str
    host: list
    username: str
    password: str
    secret: Optional[str]
    command: str

@app.post("/run-command")
def run_command(payload: DeviceCommand):
    """
    Connects to a network device using Netmiko and runs a command.
    """
    device = {
        "device_type": payload.device_type,
        "host": payload.host,
        "username": payload.username,
        "password": payload.password,
        "secret": payload.secret,
        "fast_cli": False,        # slows down but more reliable prompt detection
    "global_delay_factor": 2, # multiplies internal delays
    "conn_timeout": 10,
    "read_timeout_override": 20,
    "session_log": "netmiko_session.log",  
    }

    try:
        # Connect to the device
        with ConnectHandler(**device) as net_connect:
            if payload.secret:
                net_connect.enable()  # Enter enable mode if secret is provided
            output = net_connect.send_command(payload.command,use_textfsm=True,textfsm_template=FSM.FSMConvertor(payload.command))
        return {"status": "success", "output": output}

    except NetmikoTimeoutException:
        raise HTTPException(status_code=504, detail="Connection timed out")
    except NetmikoAuthenticationException:
        raise HTTPException(status_code=401, detail="Authentication failed")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/push-command")
def run_command(payload: Devicespush):
    """
    Connects to a network device using Netmiko and runs a command.
    """
    for i in payload.host:
        device = {
            "device_type": payload.device_type,
            "host": i,
            "username": payload.username,
            "password": payload.password,
            "secret": payload.secret,
            "fast_cli": False,        # slows down but more reliable prompt detection
        "global_delay_factor": 2, # multiplies internal delays
        "conn_timeout": 10,
        "read_timeout_override": 20,
        "session_log": "netmiko_session.log",  
        }

        try:
            # Connect to the device
            with ConnectHandler(**device) as net_connect:
                if payload.secret:
                    net_connect.enable()  # Enter enable mode if secret is provided
                output = net_connect.send_config_set(payload.command)
            return {"status": "success", "output": output}

        except NetmikoTimeoutException:
            raise HTTPException(status_code=504, detail="Connection timed out")
        except NetmikoAuthenticationException:
            raise HTTPException(status_code=401, detail="Authentication failed")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

