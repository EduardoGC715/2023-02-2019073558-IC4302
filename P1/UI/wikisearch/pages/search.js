import Head from 'next/head';
import styles from '../styles/Search.module.css';
import { useState } from 'react';
import { getLogin } from '../lib/loginAPI';
import Facet from '../components/Facet';
import FacetTable from '../components/FacetTable'
import DocumentTable from '../components/DocumentTable'
import { getMongo } from '../lib/mongoAPI';
import { useRouter } from 'next/router';

export default function Search() {
    const router = useRouter();
    if (typeof window !== 'undefined') {
        // https://developer.school/snippets/react/localstorage-is-not-defined-nextjs
        // Perform localStorage action
        const login = JSON.parse(localStorage.getItem('login'));
        // if (!login) {
        //     router.push('/index');
        // }
      }

    const [selectedEngine, setSelectedEngine] = useState("MongoAtlas");

    const handleEngineChange = (event) => {
        setSelectedEngine(event.target.value);
    };

    const facetObjectCreate = {
        PageNamespaceFacet: "None",
        PageHasRedirectFacet: "None",
        SiteInfoNameFacet: "None",
        SiteInfoDBNameFacet: "None",
        SiteLanguageFacet: "None",
        PageLastModifiedFacet: "None",
        PageLastModifiedUserFacet: "None",
        PageBytesFacet: "None",
        PageRestrictionsFacet: "None",
        PageNumberLinksFacet: "None"
    };

    const [facetObject, setFacetObject] = useState(facetObjectCreate); 

    function handleFacetChange(event, facet){
        const objectCopy = {...facetObject}
        objectCopy[facet] = event.target.value
        setFacetObject(objectCopy);
        console.log(objectCopy);
    }

    const [facetList, setFacetList] = useState({});
    const [documentList, setDocumentList] = useState([]);

    const [searchInput, setSearchInput] = useState("");
    
    function handleSearchInput(event){
        setSearchInput(event.target.value);
    }

    async function onClickSearch(){
        console.log(searchInput, selectedEngine, facetObject)
        const facetSearch = await getMongo(searchInput, facetObject)
        if (!facetSearch['facets'].length){
            alert("No documents found.");
        } else {
            setFacetList(facetSearch['facets'][0]['facet']);
            setDocumentList(facetSearch['docs']);
        }
    }

    return (
        <div className={styles.container}>
            <Head>
                <title>WikiSearch</title>
                <link rel="icon" href="/favicon.ico" />
            </Head>

            <div className={styles.grid}>
                <h1 className={styles.title}>
                    Search
                </h1>
                <div className={styles.middleSection}>
                    <input className={styles.inputT1} type="text" placeholder='Search' onChange={handleSearchInput}/>
                    <button className={styles.searchButton}><img src="/logoBusqueda.svg" onClick={onClickSearch}/></button>
                </div>

                <div>
                    <label className={styles.radioEngine}>
                        <input
                            type="radio"
                            name="radioEngineGroup"
                            value="MongoAtlas"
                            checked={selectedEngine === "MongoAtlas"}
                            onChange={handleEngineChange}
                        />
                        Mongo Atlas
                    </label>

                    <label className={styles.radioEngine}>
                        <input
                            type="radio"
                            name="radioEngineGroup"
                            value="SQL"
                            checked={selectedEngine === "SQL"}
                            onChange={handleEngineChange}
                        />
                        SQL
                    </label>
                </div>

                <div className={styles.contentGrid}>
                    <FacetTable facetList={facetList} facetObject={facetObject} handleFacetChange={handleFacetChange}/>
                    <DocumentTable documentList={documentList}/>
                </div>
                <footer>
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
        </div>
    );
}

{/* <p className={styles.facetLabel}>Page Bytes</p>
<Facet value={facetObject['PageId']} text="0" onChange={event => handleFacetChange(event, "PageId")}/>
<Facet value={facetObject['PageTitle']} text="10000" onChange={event => handleFacetChange(event, "PageTitle")}/>
<Facet value={facetObject['PageNamespace']} text="10000" onChange={event => handleFacetChange(event, "PageNamespace")}/>
<Facet value={facetObject['PageRedirect']} text="20000" onChange={event => handleFacetChange(event, "PageRedirect")}/>
<Facet value={facetObject['PageHasRedirect']} text="30000" onChange={event => handleFacetChange(event, "PageHasRedirect")}/>
<Facet value={facetObject['PageRestriction']} text="40000" onChange={event => handleFacetChange(event, "PageRestriction")}/>
<Facet value={facetObject['SiteInfoName']} text="Site Info Name" onChange={event => handleFacetChange(event, "SiteInfoName")}/>
<Facet value={facetObject['SiteInfoDBName']} text="Site Info DB Name" onChange={event => handleFacetChange(event, "SiteInfoDBName")}/>
<Facet value={facetObject['SiteLanguage']} text="Site Language" onChange={event => handleFacetChange(event, "SiteLanguage")}/>
<Facet value={facetObject['PageLastModified']} text="Page Last Modified" onChange={event => handleFacetChange(event, "PageLastModified")}/>
<Facet value={facetObject['PageLastModifiedUser']} text="Page Last Modified User" onChange={event => handleFacetChange(event, "PageLastModifiedUser")}/>
<Facet value={facetObject['PageBytes']} text="Page Bytes" onChange={event => handleFacetChange(event, "PageBytes")}/>
<Facet value={facetObject['PageText']} text="Page Text" onChange={event => handleFacetChange(event, "PageText")}/>
<Facet value={facetObject['PageWikipediaLink']} text="Page Wikipedia Link" onChange={event => handleFacetChange(event, "PageWikipediaLink")}/>
<Facet value={facetObject['PageWikipediaGenerated']} text="Page Wikipedia Generated" onChange={event => handleFacetChange(event, "PageWikipediaGenerated")}/>
<Facet value={facetObject['PageLinks']} text="Page Links" onChange={event => handleFacetChange(event, "PageLinks")}/>
<Facet value={facetObject['PageNumberLinks']} text="Page Number Links" onChange={event => handleFacetChange(event, "PageNumberLinks")}/> */}