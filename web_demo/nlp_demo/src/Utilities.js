import './index.scss';

import Container from 'react-bootstrap/Container';
import Spinner from 'react-bootstrap/Spinner';
import Popover from 'react-bootstrap/Popover';
import OverlayTrigger from 'react-bootstrap/OverlayTrigger';


const infoPopover = (info) => {
    return (
        <Popover>
            <Popover.Content> 
                {info}
            </Popover.Content>
        </Popover>
    )
}

const InfoTitle = (props) => {
    const popover = infoPopover(props.info);
    return (
        <Container className="flex flex-center">
            <span style={{paddingLeft: "1rem"}} className="pr-1">  
                <h4>{props.title}</h4>
            </span>
            <OverlayTrigger trigger="click" placement={props.infoPlacementDirection} 
                            overlay={popover}>
                <i className="bi bi-info-circle cursor-pointer" role="img" 
                   aria-label="Information"/>
            </OverlayTrigger>
        </Container>
    )
}

async function getJSONData(url = '') {
    const response = await fetch(url, {
        method: 'GET',
        mode: 'cors',
        cache: 'default',
        credentials: 'same-origin',
        headers: {
            'Content-Type': 'application/json'
        },
        redirect: 'follow',
        referrerPolicy: 'same-origin'
    });
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }
    else {
        if (response.headers.has('Content-Type')){
            if (response.headers.get('Content-Type').includes('application/json')){
                return response.json(); 
            }
            
        }
        throw new Error(`Wrong Content-Type Return`); 
    }
}

const LoadObject = (props) => {


    if (Object.keys(props.data).length === 0){
        return (
            <Container className="flex flex-center pt-3">
                <Spinner animation="border" role="status">
                    <span className="sr-only">Loading...</span>
                </Spinner>
            </Container>
        )
    }
    else if ('error' in props.data){
        return(<h5>Error: Could not load requested document.</h5>)
    }
    else {
        return (
            <div>
                {props.onSuccess()}
            </div>
        )
    }
}

export { InfoTitle, getJSONData, LoadObject };