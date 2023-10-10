import styles from '../styles/Search.module.css';
import { Fragment } from 'react';
import Highlight from './Highlight';

export default function docPreview({ key, doc }){
    
    const pageTitle = typeof doc['PageText'] !== 'undefined' ? (typeof doc['PageTitle'] !== 'object' ? doc['PageTitle'] : <Highlight highlight={doc['PageTitle']}/>) : "No title available.";
    const pageText = typeof doc['PageText'] !== "undefined" ? 
                            (typeof doc['PageText'] !== 'object' ? doc['PageText'].substring(0,150) : <Highlight highlight={doc['PageText']}/>)
                            : "No text available.";
    const PageLastModified = doc['PageLastModified'] !== null ? 
                            (typeof doc['PageLastModified'] !== 'object' ? doc['PageLastModified'] : <Highlight highlight={doc['PageLastModified']}/>)
                            : "Date not available.";
    const PageLastModifiedUser = typeof doc['PageLastModifiedUser'] !== "undefined" ? 
                            (typeof doc['PageLastModifiedUser'] !== 'object' ? doc['PageLastModifiedUser'] : <Highlight highlight={doc['PageLastModifiedUser']}/>)
                            : "User not available.";

    const PageBytes = typeof doc['PageBytes'] !== "undefined" ? 
                            doc['PageBytes']
                            : "Bytes not available.";
    const PageRedirect = typeof doc['PageRedirect'] !== "undefined" && doc['PageRedirect'] !== null ? (typeof doc['PageRedirect'] !== 'object' ? doc['PageRedirect'] : <Highlight highlight={doc['PageRedirect']}/>) : "No redirect available.";
    const PageNamespace = doc['PageNamespace'] !== null ? 
                            (typeof doc['PageNamespace'] !== 'object' ? doc['PageNamespace'] : <Highlight highlight={doc['PageNamespace']}/>)
                            : "Date not available.";
    //console.log(doc['PageLinks'], doc)
    let PageLinks;
    if (typeof doc['PageLinks'] === 'object') {
        
        if (doc['PageLinks'][0].hasOwnProperty('type')){
            PageLinks = <Highlight highlight={doc['PageLinks']}/>
        } else {
            PageLinks = doc['PageLinks'].map((link) => {
                return <span className={styles.normalText}><br />- {link[0]}</span>
            })
        }
        //console.log(doc['PageLinks'], PageLinks)
    } else {
        PageLinks = "No links available."
    }
    
    

                            //console.log(PageLastModified, doc['PageLastModified']);
    return <Fragment key={key}>
        <p className={styles.docTitle}>{pageTitle}       </p>
        <p className={styles.normalText}>by {PageLastModifiedUser} on {PageLastModified}</p>
        <p className={styles.pageText}>...{pageText}...</p>
        <p className={styles.normalText}>Redirect: {PageRedirect}</p>
        <p className={styles.normalText}>Namespace: {PageNamespace} Bytes: {PageBytes}<br />PageLinks: {PageLinks}</p>
    </Fragment>
}