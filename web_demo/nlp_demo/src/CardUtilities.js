import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Badge from 'react-bootstrap/Badge';
import OverlayTrigger from 'react-bootstrap/OverlayTrigger';
import Popover from 'react-bootstrap/Popover';
import Button from 'react-bootstrap/Button';
import Card from 'react-bootstrap/Card';


const TranslationText = (props) => {
    if (typeof props.translation !== 'undefined') {
        return (
            <div>
                <p>{props.text}</p>
                <OverlayTrigger trigger="click" placement="top" 
                                overlay={<Popover>
                                            <Popover.Content>
                                                {props.translation}
                                            </Popover.Content>
                                        </Popover>}>
                    <Button>Translation</Button>
                </OverlayTrigger>
            </div>
        )
    }
    else {
        return <p>{props.text}</p>
    }

}

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
        <div className="flex">
            <Card.Title className="text-center flex-grow-1" 
                        style={{paddingLeft: "1rem"}}>
                <h3>{props.title}</h3>
            </Card.Title>
            <OverlayTrigger trigger="click" placement="left" 
                            overlay={popover}>
                <i className="bi bi-info-circle" role="img" 
                   aria-label="Information"/>
            </OverlayTrigger>
        </div>
    )
}

const CardLabel = (props) => {
    return (
        <Container className="card-label-container">
            <Row>
                <Col className="card-label-names card-label-col" 
                    sm={4} md={{ span: 3, offset: 1 }}>
                    <h4>Input</h4>
                </Col>
                <Col sm={8} md={{ span: 7}} 
                     className="card-label-col card-label-input-value">
                    <TranslationText text={props.text} translation={props.translation}/>
                </Col>
            </Row>
            <Row>
                <Col className="card-label-names card-label-col no-top-border" 
                    sm={4} md={{ span: 3, offset: 1 }} >
                    <h4>Output</h4>
                </Col>
                <Col className="card-label-output-value card-label-col no-top-border" 
                    sm={8} md={{ span: 7}} >
                    <h4>
                        <Badge variant="primary">{props.label}</Badge>
                    </h4>
                </Col>
            </Row>
        </Container>
    )
}

export { CardLabel, InfoTitle };