import styles from '../styles/Search.module.css';
import { Fragment } from 'react';
import Highlight from './Highlight';
import Link from 'next/link'

export default function docPreviewAutonomous({ key, doc, searchQuery, searchEngine }){
    
    console.log(doc);
    const pageTitle = typeof doc['PageTitle'] !== 'undefined' ? doc['PageTitle'] : "No title available.";

    const pageText = typeof doc['PageText'] !== "undefined" ? doc['PageText'].substring(0,150) : "No text available.";

    const PageLastModified = doc['PageLastModified'] !== null ? doc['PageLastModified'] : "Date not available.";

    const PageLastModifiedUser = typeof doc['PageLastModifiedUser'] !== "undefined" ? doc['PageLastModifiedUser'] : "User not available.";

    const PageBytes = typeof doc['PageBytes'] !== "undefined" ? doc['PageBytes'] : "Bytes not available.";
   
    const PageRedirect = typeof doc['PageRedirect'] !== "undefined" && doc['PageRedirect'] !== null ? doc['PageRedirect'] : "No redirect available.";
   
    const PageNamespace = doc['PageNamespace'] !== null ? doc['PageNamespace'] : "Date not available.";

    let PageLinks;
    if (typeof doc['PageLinks'] === 'string' && doc['PageLinks'].trim() !== '') { // check if PageLinks is a non-empty string

        const linksArray = doc['PageLinks'].split(','); // Split the string into an array based on commas

        // Map the links and wrap each in a span
        PageLinks = linksArray.map((link) => {
            return <span className={styles.normalText}><br />- {link.trim()}</span> // Trim to remove any extra whitespace
        });
    } else {
        PageLinks = "No links available."
    }

    //console.log(PageLastModified, doc['PageLastModified']);
    return <Fragment key={key}>
        <Link href={{pathname: '/docView', query:{id: doc['PageTitleKey'], searchQuery, searchEngine}}}><p className={styles.docTitle}>{pageTitle}</p></Link>
        <p className={styles.normalText}>by {PageLastModifiedUser} on {PageLastModified}</p>
        <p className={styles.pageText}>...{pageText}...</p>
        <p className={styles.normalText}>Redirect: {PageRedirect}</p>
        <p className={styles.normalText}>Namespace: {PageNamespace} Bytes: {PageBytes}<br />PageLinks: {PageLinks}</p>
    </Fragment>
}