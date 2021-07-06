import './_contact.scss';
import './index.scss';

import Col from 'react-bootstrap/Col';
import Row from 'react-bootstrap/Row';

function Contact(){

    return(
        <div className="contacts-div extra-width-padding" id="full-width" >
            <Row>
                <Col md={12} lg={6}>
                    <p className="bold">Related Links:</p>
                    <ul>
                        <li><a href="http://ucrel.lancs.ac.uk/">University Centre for Computer Corpus Research on Language (UCREL)</a></li>
                        <li><a href="https://www.lancaster.ac.uk/scc/research/data-science/">Data Science Group</a></li>
                        <li><a href="https://www.lancaster.ac.uk/dsi/">Data Science Institute</a></li>
                        <li><a href="https://www.lancaster.ac.uk/scc/">School of Computing and Communications (SCC)</a></li>
                        <li><a href="https://www.lancaster.ac.uk/">Lancaster University</a></li>
                    </ul>
                </Col>
                <Col md={12} lg={6}>
                    <p className="bold">Contact Us:</p>
                    <address>
                        <ul>
                            <li>Email: <a href="mailto:ucrel@lancaster.ac.uk">ucrel@lancaster.ac.uk</a></li>
                            <li>Telephone: <a href="tel:+441524510357">+44 1524 510357</a></li>
                            <li>Twitter: <a href="https://twitter.com/UCREL_NLP">@UCREL_NLP</a> and <a href="https://twitter.com/ucrelcrs">@ucrelcrs</a></li>
                            <li>Physical Address: <a href="https://www.google.com/maps/place/InfoLab21,+South+Dr,+Bailrigg,+Lancaster+LA1+4WA/@54.005554,-2.784785,17z/data=!3m1!4b1!4m5!3m4!1s0x487b6303b899a6ab:0x9cdaf6b2f739c94c!8m2!3d54.005554!4d-2.784785?hl=en">B50, School of Computing and Communications, InfoLab21, Lancaster University, Lancaster, United Kingdom, LA1 4WA</a></li>
                        </ul>
                    </address>

                </Col>
            </Row>
        </div>
    )
}

export default Contact