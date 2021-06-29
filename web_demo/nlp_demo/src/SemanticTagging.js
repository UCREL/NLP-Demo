import React, { useState, useEffect } from 'react';

import Container from 'react-bootstrap/Container';

import UCRELDoc from './UCRELDoc';
import {getJSONData, LoadObject} from './Utilities';

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

    function ucrelDoc(){
        return(<UCRELDoc tokens={ucrelData.tokens} 
                         sentenceIndexes={ucrelData.sentence_indexes}/>)
    }
    

    return(
        <Container className="extra-height-padding alternative-color" id="full-width">
            <h1>Semantic Tagging</h1>
            <p className="lead-text-muted">
                The task of predicting the broad dictionary sense for 
                each word in a given text.
            </p>
            <hr />
            <SemanticTagKey/>
            <hr />
            <LoadObject data={ucrelData} onSuccess={ucrelDoc}/>

            
        </Container>
    )
} 

export default SemanticTagging; 