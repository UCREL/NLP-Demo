import React, { useState } from 'react';
import franc from 'franc';
import { iso6393 } from 'iso-639-3'
import { VictoryAxis, VictoryBar, VictoryChart, VictoryTheme, VictoryTooltip } from 'victory';

import Container from "react-bootstrap/Container"
import Form from 'react-bootstrap/Form';

const DemoCard = () => {

    const francDetection = (text) => {
        
        const langCodeToData = (code) => {
            return iso6393.find((languageData) => languageData['iso6393']===code);
        }
        
        const francToProbabilities = (francValues) => {
            const exponents = francValues.map((x) => {return Math.exp(x[1]);});
            const total = exponents.reduce((a, b) => a + b, 0);
            return francValues.map((x) => {return [x[0], Math.exp(x[1]) / total];})
        }

        const francChartData = (francProbabilities) => {
            const [francCode, francProbability] = francProbabilities;
            const languageData = langCodeToData(francCode);
            const language = languageData.name;
            const francData = Object.assign(languageData, 
                                            {Probability: francProbability, label: language});
            return francData

        }

        const francAll = francToProbabilities(franc.all(text))
                         .map(francChartData)
                         .sort((a,b) => {return b['Probability']-a['Probability']})
                         .slice(0,5);
        return francAll;
    }

    const [inputText] = useState("Lancaster University");
    const [identifiedLanguage, setIdentifiedLanguage] = useState(francDetection(inputText));
    const inputTextArea = React.createRef();



    const identifyLanguage = () => {
        const newInputText = inputTextArea.current.value;
        setIdentifiedLanguage(francDetection(newInputText));
    }
    
    return (
        <Container>
            <p className="mb-3 mt-3">This uses the Franc language detection javascript library, it can 
            detect languages. It uses a character tri-gram model, to find 
            distances between the given input and pre-computed tri-gram statistics 
            from the languages. The output is a distance measure rather than a 
            probability, whereby all language distances are normalised based on 
            the closet language match. 
            </p>
            <hr/>
            <Form>
                <Form.Group controlId="inputTextLangDetect">
                    <Form.Label className="bold">Input:</Form.Label>
                    <Form.Control as="textarea" rows={3} spellCheck={true}
                                  ref={inputTextArea} 
                                  placeholder={inputText} onKeyUp={identifyLanguage} />
                    <Form.Text className="text-muted">
                        Input text for it's language to be detected.
                    </Form.Text>
                </Form.Group>
            </Form>
            <VictoryChart 
                theme={VictoryTheme.grayscale}
                domainPadding={{x: [8, 0], y: [0,0]}}
            >
                <VictoryAxis />
                <VictoryAxis 
                    dependentAxis tickFormat={(x) => (`${x * 100}%`)}
                />
                <VictoryBar 
                    labelComponent={<VictoryTooltip orientation="top" pointerLength={0} />}
                    sortOrder="ascending"
                    sortKey = "y"
                    horizontal x="iso6392B" y="Probability" 
                    data={identifiedLanguage} 
                />
            </VictoryChart>
        </Container>
    )
}

export default DemoCard;