import Head from 'next/head';
import styles from '../styles/DocView.module.css';
import { useEffect, useState } from 'react';
import { useRouter } from 'next/router';
import Link from 'next/link';
import { getMongoDocument } from '../lib/mongoAPI';
import { getAutonomousDocument } from '../lib/autonomousAPI';
import Highlight from '../components/Highlight';


export async function getServerSideProps(context){
    const data = context.query;
    const id = data['id'];
    const searchQuery = data['searchQuery'];
    const searchEngine = data['searchEngine'];

    return { props: { id, searchEngine, searchQuery } }
}
// preguntar de esto
export default function DocView({id, searchEngine, searchQuery}){
    const router = useRouter();
    const [info, setInfo] = useState({
        PageTitle: "Loading...",
        PageText: "Loading...",
        PageLastModified: "Loading...",
        PageLastModifiedUser: "Loading...",
        PageBytes: "Loading...",
        PageRedirect: "Loading...",
        PageNamespace: "Loading...",
        PageHasRedirect: "Loading...",
        SiteInfoName: "Loading...",
        SiteInfoDBName: "Loading...",
        SiteLanguage: "Loading...",
        PageWikipediaLink: "Loading...",
        PageWikipediaGenerated: "Loading...",
        PageNumberLinks: "Loading...",
        PageLinks: "Loading...",
        PageRestrictions: "Loading..."
    })

    useEffect(() => {
        const fetchData = async () => {
            let doc;
            if (searchEngine === "MongoAtlas") {
              doc = await getMongoDocument(id, searchQuery);
            } else {
              doc = await getAutonomousDocument(id);
            }
            const newInfo = {}
            newInfo.PageTitle = typeof doc['PageTitle'] !== 'undefined' && doc['PageTitle'] !== null ? (typeof doc['PageTitle'] !== 'object' ? doc['PageTitle'] : <Highlight highlight={doc['PageTitle']} key={`PageTitle${doc['_id']}`}/>) : "No title available.";
            newInfo.PageText = typeof doc['PageText'] !== "undefined" && doc['PageText'] !== null ? 
                                    (typeof doc['PageText'] !== 'object' ? doc['PageText'] : <Highlight highlight={doc['PageText']} key={`PageText${doc['_id']}`}/>)
                                    : "No text available.";
            newInfo.PageLastModified = doc['PageLastModified'] !== null && doc['PageText'] !== null ? 
                                    (typeof doc['PageLastModified'] !== 'object' ? doc['PageLastModified'] : <Highlight highlight={doc['PageLastModified']} key={`PageLastModified${doc['_id']}`}/>)
                                    : "Date not available.";
            newInfo.PageLastModifiedUser = typeof doc['PageLastModifiedUser'] !== "undefined" && doc['PageText'] !== null ? 
                                    (typeof doc['PageLastModifiedUser'] !== 'object' ? doc['PageLastModifiedUser'] : <Highlight highlight={doc['PageLastModifiedUser']} key={`PageLastModifiedUser${doc['_id']}`}/>)
                                    : "User not available.";
        
            newInfo.PageBytes = typeof doc['PageBytes'] !== "undefined" && doc['PageText'] !== null ? 
                                    doc['PageBytes']
                                    : "Bytes not available.";
            newInfo.PageRedirect = typeof doc['PageRedirect'] !== "undefined" && doc['PageRedirect'] !== null ? (typeof doc['PageRedirect'] !== 'object' ? doc['PageRedirect'] : <Highlight highlight={doc['PageRedirect']} key={`PageRedirect${doc['_id']}`}/>) : "No redirect available.";
            newInfo.PageNamespace = typeof doc['PageNamespace'] !== "undefined" && doc['PageNamespace'] !== null ? 
                                    (typeof doc['PageNamespace'] !== 'object' ? doc['PageNamespace'] : <Highlight highlight={doc['PageNamespace']} key={`PageNamespace${doc['_id']}`}/>)
                                    : "Date not available.";
        
            newInfo.PageHasRedirect = typeof doc['PageHasRedirect'] !== "undefined" && doc['PageHasRedirect'] !== null ?
                                        (typeof doc['PageHasRedirect'] !== 'object' ? doc['PageHasRedirect'] : <Highlight highlight={doc['PageHasRedirect']} key={`PageHasRedirect${doc['_id']}`}/>)
                                        : "No information whether it has a redirect available.";
            newInfo.SiteInfoName = typeof doc['SiteInfoName'] !== "undefined" && doc['SiteInfoName'] !== null ?
                                        (typeof doc['SiteInfoName'] !== 'object' ? doc['SiteInfoName'] : <Highlight highlight={doc['SiteInfoName']} key={`SiteInfoName${doc['_id']}`}/>)
                                        : "No Site Info Name available.";
            newInfo.SiteInfoDBName = typeof doc['SiteInfoDBName'] !== "undefined" && doc['SiteInfoDBName'] !== null ?
                                        (typeof doc['SiteInfoDBName'] !== 'object' ? doc['SiteInfoDBName'] : <Highlight highlight={doc['SiteInfoDBName']} key={`SiteInfoDBName${doc['_id']}`}/>)
                                        : "No Site Info Data Base Name available.";
            newInfo.SiteLanguage = typeof doc['SiteLanguage'] !== "undefined" && doc['SiteLanguage'] !== null ?
                                        (typeof doc['SiteLanguage'] !== 'object' ? doc['SiteLanguage'] : <Highlight highlight={doc['SiteLanguage']} key={`SiteLanguage${doc['_id']}`}/>)
                                        : "No Site Language available.";
            newInfo.PageWikipediaLink = typeof doc['PageWikipediaLink'] !== "undefined" && doc['PageWikipediaLink'] !== null ?
                                        (typeof doc['PageWikipediaLink'] !== 'object' ? doc['PageWikipediaLink'] : <Highlight highlight={doc['PageWikipediaLink']} key={`PageWikipediaLink${doc['_id']}`}/>)
                                        : "No Wikipedia link available.";
            newInfo.PageWikipediaGenerated = typeof doc['pageWikipediaGenerated'] !== "undefined" && doc['pageWikipediaGenerated'] !== null ?
                                        (typeof doc['pageWikipediaGenerated'] !== 'object' ? doc['pageWikipediaGenerated'] : <Highlight highlight={doc['pageWikipediaGenerated']} key={`pageWikipediaGenerated${doc['_id']}`}/>)
                                        : "No Wikipedia generated link available.";
            newInfo.PageNumberLinks = typeof doc['PageNumberLinks'] !== "undefined" && doc['PageNumberLinks'] !== null ? 
                                        (typeof doc['PageNumberLinks'] !== 'object' ? doc['PageNumberLinks'] : <Highlight highlight={doc['PageNumberLinks']} key={`PageNumberLinks${doc['_id']}`}/>)
                                        : "No number of links available";
            
            if (searchEngine === "MongoAtlas" && typeof doc['PageLinks'] === 'object') {
                // const linkKeys = Object.keys(doc['PageLinks']);
                // PageLinks = linkKeys.map((link) => {
                //     const linkArrayKeys = Object.keys(doc['PageLinks'][link]);
                //     return linkArrayKeys.map((element) => {
                //         let anchor;
                //         if (typeof doc['PageLinks'][link][element] === 'object') {
                //             anchor = <Highlight highlight={doc['PageLinks'][link][element]} key={`PageLinks${doc['_id']}`}/>
                //         } else {
                //             anchor = <span className={styles.normalText}><br />- {doc['PageLinks'][link][element]}</span>
                //         }
                //         return <span className={styles.normalText}><br />- {anchor} | <a href={doc['PageLinks'][link][element]}>{doc['PageLinks'][link][element]}</a></span>
                //     })
                // })
                newInfo.PageLinks = doc['PageLinks'].map((link) => {let anchor;
                        if (typeof link[0] === 'object') {
                            anchor = <Highlight highlight={link[0]} key={`PageLinks`}/>
                        } else {
                            anchor = <span className={styles.normalText}>{link[0]}</span>
                        }
                        return <span className={styles.normalText}><br />- {anchor} | <a href={link[1]}>{link[1]}</a></span>
                    })
                //console.log(doc['PageLinks'], PageLinks, typeof PageLinks)
            } else if(searchEngine === "SQL" && doc['PageLinks'] !== null && doc['PageLinks'].trim() !== ''){
                const linkTexts = doc['PageLinks'].split(','); // Split the string into an array based on commas
                const linkHrefs = doc['PageLinksLinks'].split(','); // Split the string into an array based on commas
                // Map the links and wrap each in a span
                newInfo.PageLinks = linkTexts.map((linkText, index) => {
                    return (
                        <span className={styles.normalText}>
                            <br />- {linkText} | <a href={linkHrefs[index]}>{linkHrefs[index]}</a>
                        </span>
                    );
                });
            }else {
                newInfo.PageLinks = "No links available."
            }
        
            if (searchEngine === "MongoAtlas" && typeof doc['PageRestrictions'] === 'object' && doc['PageRestrictions'].length !== 0) {
                
                if (doc['PageRestrictions'][0].hasOwnProperty('type')){
                    newInfo.PageRestrictions = <Highlight highlight={doc['PageRestrictions']} key={`PageRestrictions`}/>
                } else {
                    newInfo.PageRestrictions = doc['PageRestrictions'].map((link) => {
                        return <span className={styles.normalText}><br />- {link[0]}</span>
                    })
                }
                //console.log(doc['PageLinks'], PageLinks)
            } else if(searchEngine === "SQL" &&  doc['PageRestrictions'] !== 0){
                const restrictionsArray = doc['PageRestrictions'].split(','); // Split the string into an array based on commas
                newInfo.PageRestrictions = restrictionsArray.map((restriction) => {
                    return (<span className={styles.normalText}><br />- {restriction}</span>
                    );
                });
            }else {
                newInfo.PageRestrictions = "No restrictions available."
            }
            setInfo(newInfo);
        };
        
        fetchData(); // Call the function to fetch the data
        
    }, [searchEngine, id, searchQuery]);

    function logOut(){
        localStorage.removeItem('login');
        router.push('/');
    }

    return (
        <div className={styles.container}>
            <Head>
                <title>Document View</title>
                <link rel="icon" href="/favicon.ico" />
            </Head>

            <h1 className={styles.title}>Document View</h1>
            <h2 className={styles.docTitle}>{info.PageTitle}</h2>
            <p className={styles.subtitle}>{info.PageLastModified} by {info.PageLastModifiedUser}</p>
            <p className={styles.normalText}>Wikipedia Link: <Link href={info.PageWikipediaLink} target="_blank">{info.PageWikipediaLink}</Link></p>
            <p className={styles.normalText}>Wikipedia Generated Link: <Link href={info.PageWikipediaGenerated} target="_blank">{info.PageWikipediaGenerated}</Link></p>
            <h3>Document Info:</h3>
            <ul>
                <li>Bytes: {info.PageBytes}</li>
                <li>Namespace: {info.PageNamespace}</li>
                <li>Has Redirect: {info.PageHasRedirect}</li>
                <li>Redirect: {info.PageRedirect}</li>
                <li>Restrictions: {info.PageRestrictions}</li>
                <li>Site Info Name: {info.SiteInfoName}</li>
                <li>Site Info Data Base Name: {info.SiteInfoDBName}</li>
                <li>Site Language: {info.SiteLanguage}</li>
            </ul>
            <p>Number of links: {info.PageNumberLinks}. Links: {info.PageLinks}</p>
            <h2>Text</h2>
            <p className={styles.pageText}>{info.PageText}</p>
            <div className={styles.buttonDiv}>
                <button className={styles.buttonT1} onClick={() => {router.push('/search')}}>Return to Search</button>
            </div>
            <footer className={styles.footerDoc}>
                <button className={styles.logOutButton} onClick={logOut}>Log Out</button>
                <a
                    href="https://vercel.com?utm_source=create-next-app&utm_medium=default-template&utm_campaign=create-next-app"
                    target="_blank"
                    rel="noopener noreferrer"
                >
                    Powered by{' '}
                    <img src="/vercel.svg" alt="Vercel" className={styles.logo} />
                </a>
            </footer>
        </div>
    );
}