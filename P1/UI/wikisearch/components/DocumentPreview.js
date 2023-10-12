import styles from '../styles/Search.module.css';
import { Fragment } from 'react';
import Highlight from './Highlight';
import Link from 'next/link'

export default function docPreview({ key, doc, searchQuery, searchEngine }){
    console.log(key, doc);
    
    const pageTitle = typeof doc['PageText'] !== 'undefined' ? (typeof doc['PageTitle'] !== 'object' ? doc['PageTitle'] : <Highlight highlight={doc['PageTitle']} key={`PageTitle${doc['_id']}`}/>) : "No title available.";
    const pageText = typeof doc['PageText'] !== "undefined" ? 
                            (typeof doc['PageText'] !== 'object' ? doc['PageText'].substring(0,150) : <Highlight highlight={doc['PageText']} key={`PageText${doc['_id']}`}/>)
                            : "No text available.";
    const PageLastModified = doc['PageLastModified'] !== null ? 
                            (typeof doc['PageLastModified'] !== 'object' ? doc['PageLastModified'] : <Highlight highlight={doc['PageLastModified']} key={`PageLastModified${doc['_id']}`}/>)
                            : "Date not available.";
    const PageLastModifiedUser = typeof doc['PageLastModifiedUser'] !== "undefined" ? 
                            (typeof doc['PageLastModifiedUser'] !== 'object' ? doc['PageLastModifiedUser'] : <Highlight highlight={doc['PageLastModifiedUser']} key={`PageLastModifiedUser${doc['_id']}`}/>)
                            : "User not available.";

    const PageBytes = typeof doc['PageBytes'] !== "undefined" ? 
                            doc['PageBytes']
                            : "Bytes not available.";
    const PageRedirect = typeof doc['PageRedirect'] !== "undefined" && doc['PageRedirect'] !== null ? (typeof doc['PageRedirect'] !== 'object' ? doc['PageRedirect'] : <Highlight highlight={doc['PageRedirect']} key={`PageRedirect${doc['_id']}`}/>) : "No redirect available.";
    const PageNamespace = doc['PageNamespace'] !== null ? 
                            (typeof doc['PageNamespace'] !== 'object' ? doc['PageNamespace'] : <Highlight highlight={doc['PageNamespace']} key={`PageNamespace${doc['_id']}`}/>)
                            : "Date not available.";
    
    let PageLinks;
    if (typeof doc['PageLinks'] === 'object') {
        
        if (doc['PageLinks'][0].hasOwnProperty('type')){
            PageLinks = <Highlight highlight={doc['PageLinks']} key={`PageLinks${doc['_id']}`}/>
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
        <Link href={{pathname: '/docView', query:{id: doc['_id'], searchQuery, searchEngine}}}><p className={styles.docTitle}>{pageTitle}</p></Link>
        <p className={styles.normalText}>by {PageLastModifiedUser} on {PageLastModified}</p>
        <p className={styles.pageText}>...{pageText}...</p>
        <p className={styles.normalText}>Redirect: {PageRedirect}</p>
        <p className={styles.normalText}>Namespace: {PageNamespace} Bytes: {PageBytes}<br />PageLinks: {PageLinks}</p>
    </Fragment>
}