import React, { useState, useEffect } from 'react';

import Container from 'react-bootstrap/Container';
import Spinner from 'react-bootstrap/Spinner';

import UCRELDoc from './UCRELDoc';

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

const UCRELSpinner = (props) => {
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
        return(<h5>Error: Example document not in the correct location.</h5>)
    }
    else {
        return(<UCRELDoc tokens={props.data.tokens} sentenceIndexes={props.data.sentence_indexes}/>);
    }
}

function KeyBoxes(props) {
    return (
        <span>
            <span className="key-icon">
                <svg viewBox="0 0 10 10" id={props._id}>
                    <rect x="0" y="0" width="100%" height="100%"/>
                </svg>
            </span>
            <span className="pl-2 key-text">{props._key}</span>
        </span>
    )
}

function SemanticTagKey() {
    // For the CSS tags see the `_ucrel.scss` file.
    const css_id_to_usas_tag = {"E1": "Emotion", "N3": "Measurement", 
                                "Z1": "Name", "N1": "Number", "T1": "Time"};
    const keyBoxes = [];
    for (let css_id in css_id_to_usas_tag){
        const usas_tag = css_id_to_usas_tag[css_id];
        keyBoxes.push(<KeyBoxes  _id={css_id} _key={usas_tag} key={css_id} />);
    }

    return (
        
        <div className="pb-2">
            <h4 className="pt-2 pb-1 center-text"> Semantic Tag Key </h4>
            <div className="flex-wrap flex-space-evenly">
                {keyBoxes}
            </div>
        </div>
    )
}

function SemanticTagging() {
    const [ucrelData, setUcrelData] = useState({})
    
    useEffect( () => {
        if (Object.keys(ucrelData).length === 0){
            getJSONData(process.env.PUBLIC_URL + '/data/usas_example.json')
            .then(setUcrelData)
            .catch(() => {setUcrelData({'error': true})});
        }
    }, [ucrelData])

    

    return(
        <Container className="full-height" id="full-width">
            <h1>Semantic Tagging</h1>
            <p className="lead text-muted">
                The task of predicting the broad dictionary sense for 
                each word in a given text.
            </p>
            <hr />
            <SemanticTagKey/>
            <hr />
            <UCRELSpinner data={ucrelData} />

            
        </Container>
    )
} 

export default SemanticTagging; 