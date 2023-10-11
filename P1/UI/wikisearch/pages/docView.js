import Head from 'next/head';
import styles from '../styles/DocView.module.css';
import { useEffect, useState } from 'react';
import { useRouter } from 'next/router';
import Link from 'next/link';
import { getMongoDocument } from '../lib/mongoAPI';
import Highlight from '../components/Highlight';


export async function getServerSideProps(context){
    const data = context.query;
    const id = data['id'];
    const searchQuery = data['searchQuery'];
    const searchEngine = data['searchEngine'];

    const doc = await getMongoDocument(id, searchQuery, searchEngine);
    return { props: { doc } }
}

export default function DocView({doc}){
    const router = useRouter();

    console.log(doc)
    const PageTitle = typeof doc['PageText'] !== 'undefined' ? (typeof doc['PageTitle'] !== 'object' ? doc['PageTitle'] : <Highlight highlight={doc['PageTitle']}/>) : "No title available.";
    const PageText = typeof doc['PageText'] !== "undefined" ? 
                            (typeof doc['PageText'] !== 'object' ? doc['PageText'] : <Highlight highlight={doc['PageText']}/>)
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

    const PageHasRedirect = typeof doc['PageHasRedirect'] !== "undefined" && doc['PageHasRedirect'] !== null ?
                                (typeof doc['PageHasRedirect'] !== 'object' ? doc['PageHasRedirect'] : <Highlight highlight={doc['PageHasRedirect']}/>)
                                : "No information whether it has a redirect available.";
    const SiteInfoName = typeof doc['SiteInfoName'] !== "undefined" && doc['SiteInfoName'] !== null ?
                                (typeof doc['SiteInfoName'] !== 'object' ? doc['SiteInfoName'] : <Highlight highlight={doc['SiteInfoName']}/>)
                                : "No Site Info Name available.";
    const SiteInfoDBName = typeof doc['SiteInfoDBName'] !== "undefined" && doc['SiteInfoDBName'] !== null ?
                                (typeof doc['SiteInfoDBName'] !== 'object' ? doc['SiteInfoDBName'] : <Highlight highlight={doc['SiteInfoDBName']}/>)
                                : "No Site Info Data Base Name available.";
    const SiteLanguage = typeof doc['SiteLanguage'] !== "undefined" && doc['SiteLanguage'] !== null ?
                                (typeof doc['SiteLanguage'] !== 'object' ? doc['SiteLanguage'] : <Highlight highlight={doc['SiteLanguage']}/>)
                                : "No Site Language available.";
    const PageWikipediaLink = typeof doc['PageWikipediaLink'] !== "undefined" && doc['PageWikipediaLink'] !== null ?
                                (typeof doc['PageWikipediaLink'] !== 'object' ? doc['PageWikipediaLink'] : <Highlight highlight={doc['PageWikipediaLink']}/>)
                                : "No Wikipedia link available.";
    const PageWikipediaGenerated = typeof doc['pageWikipediaGenerated'] !== "undefined" && doc['pageWikipediaGenerated'] !== null ?
                                (typeof doc['pageWikipediaGenerated'] !== 'object' ? doc['pageWikipediaGenerated'] : <Highlight highlight={doc['pageWikipediaGenerated']}/>)
                                : "No Wikipedia generated link available.";
    const PageNumberLinks = typeof doc['PageNumberLinks'] !== "undefined" && doc['PageNumberLinks'] !== null ? 
                                (typeof doc['PageNumberLinks'] !== 'object' ? doc['PageNumberLinks'] : <Highlight highlight={doc['PageNumberLinks']}/>)
                                : "No number of links available.";
    let PageLinks;
    if (typeof doc['PageLinks'] === 'object') {
        
        if (doc['PageLinks'][0].hasOwnProperty('type')){
            PageLinks = <Highlight highlight={doc['PageLinks']} key={`PageLinks${doc['_id']}`}/>
        } else {
            PageLinks = doc['PageLinks'].map((link) => {
                return <span className={styles.normalText}><br />- {link[0]} | <a href={link[1]}>{link[1]}</a></span>
            })
        }
        //console.log(doc['PageLinks'], PageLinks)
    } else {
        PageLinks = "No links available."
    }
    let PageRestrictions;
    if (typeof doc['PageRestrictions'] === 'object' && doc['PageRestrictions'].length !== 0) {
        
        if (doc['PageRestrictions'][0].hasOwnProperty('type')){
            PageRestrictions = <Highlight highlight={doc['PageRestrictions']} key={`PageRestrictions${doc['_id']}`}/>
        } else {
            PageRestrictions = doc['PageRestrictions'].map((link) => {
                return <span className={styles.normalText}><br />- {link[0]}</span>
            })
        }
        //console.log(doc['PageLinks'], PageLinks)
    } else {
        PageRestrictions = "No restrictions available."
    }

    return (
        <div className={styles.container}>
            <Head>
                <title>Document View</title>
                <link rel="icon" href="/favicon.ico" />
            </Head>

            <h1 className={styles.title}>Document View</h1>
            <h2 className={styles.docTitle}>{PageTitle}</h2>
            <p className={styles.subtitle}>{PageLastModified} by {PageLastModifiedUser}</p>
            <p className={styles.normalText}>Wikipedia Link: <Link href={PageWikipediaLink}>{PageWikipediaLink}</Link></p>
            <p className={styles.normalText}>Wikipedia Generated Link: <Link href={PageWikipediaGenerated}>{PageWikipediaGenerated}</Link></p>
            <h3>Document Info:</h3>
            <ul>
                <li>Bytes: {PageBytes}</li>
                <li>Namespace: {PageNamespace}</li>
                <li>Has Redirect: {PageHasRedirect}</li>
                <li>Redirect: {PageRedirect}</li>
                <li>Restrictions: {PageRestrictions}</li>
                <li>Site Info Name: {SiteInfoName}</li>
                <li>Site Info Data Base Name: {SiteInfoDBName}</li>
                <li>Site Language: {SiteLanguage}</li>
            </ul>
            <p>Links: {PageLinks}</p>
            <h2>Text</h2>
            <p className={styles.pageText}>{PageText}</p>
            <div className={styles.buttonDiv}>
                <button className={styles.buttonT1} onClick={() => {router.push('/search')}}>Return to Search</button>
            </div>
            

        </div>
    );
}