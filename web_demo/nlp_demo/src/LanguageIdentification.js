import { useState } from 'react';

import Container from 'react-bootstrap/Container';
import Card from 'react-bootstrap/Card';
import Nav from 'react-bootstrap/Nav';
import Tab from 'react-bootstrap/Tab';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';

import StandardCard from './StandardCard';
import CodeMixedCard from './CodeMixedCard';
import DialectCard from './DialectCard';
import DemoCard from './DemoCard';

const LanguageIdentification = () => {

    const [showTitleInfo, setShowTitleInfo] = useState(false);
    const [showTranslationText, setShowTranslationText] = useState(false);

    const onNavSelect = () => {
        setShowTitleInfo(false);
        setShowTranslationText(false);
    }

    return(
        <div className="extra-height-padding" id="full-width">
            <Col xs={12} xl={{span: 8, offset: 2}}>
                <h1>Language Identification</h1>
                <p className="lead-text-muted">
                    The task of predicting the language of a given text.
                </p>
                <hr/>
                <Row className="pt-2">
                    <Col xl={{ span: 8, offset: 2 }}>
                    <Tab.Container defaultActiveKey="standard">
                        <Card className="mx-auto">
                            <Card.Header>
                                <Nav variant="tabs" 
                                    onSelect={onNavSelect}>
                                    <Nav.Item>
                                        <Nav.Link eventKey="standard">
                                            Standard
                                        </Nav.Link>
                                    </Nav.Item>
                                    <Nav.Item>
                                        <Nav.Link eventKey="codemixed">
                                            Codemixed
                                        </Nav.Link>
                                    </Nav.Item>
                                    <Nav.Item>
                                        <Nav.Link eventKey="dialects">
                                            Dialects
                                        </Nav.Link>
                                    </Nav.Item>
                                    <Nav.Item>
                                        <Nav.Link eventKey="demo">
                                            Demo
                                        </Nav.Link>
                                    </Nav.Item>
                                </Nav>
                            </Card.Header>

                            <Tab.Content>
                                <Tab.Pane eventKey="standard">
                                    <StandardCard showTitleInfo={showTitleInfo} 
                                                setShowTitleInfo={setShowTitleInfo}/>
                                </Tab.Pane>
                                <Tab.Pane eventKey="codemixed">
                                    <CodeMixedCard showTitleInfo={showTitleInfo} 
                                                setShowTitleInfo={setShowTitleInfo}
                                                showTranslationText={showTranslationText}
                                                setShowTranslationText={setShowTranslationText}
                                                />
                                </Tab.Pane>
                                <Tab.Pane eventKey="dialects">
                                    <DialectCard showTitleInfo={showTitleInfo} 
                                                setShowTitleInfo={setShowTitleInfo}/>
                                </Tab.Pane>
                                <Tab.Pane eventKey="demo">
                                    <DemoCard />
                                </Tab.Pane>
                            </Tab.Content>
                            
                        </Card>
                    </Tab.Container>
                    </Col>
                </Row>
            </Col>
        </div>
    )
}

export default LanguageIdentification;