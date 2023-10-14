
export async function getAutonomous(searchInput, facetObject){
    try{
      const list = [];
      list.push(facetObject["PageLastModifiedUserFacet"] == "None" ? "" : facetObject["PageLastModifiedUserFacet"]);
      list.push(facetObject["PageNamespaceFacet"] == "None" ? "" : facetObject["PageNamespaceFacet"]);
      list.push(facetObject["SiteInfoNameFacet"] == "None" ? "" : facetObject["SiteInfoNameFacet"]);
      list.push(facetObject["SiteInfoDBNameFacet"] == "None" ? "" : facetObject["SiteInfoDBNameFacet"]);
      list.push(facetObject["SiteLanguageFacet"] == "None" ? "" : facetObject["SiteLanguageFacet"]);
      list.push(facetObject["PageRestrictionsFacet"]  == "None" ? "" : facetObject["PageRestrictionsFacet"]);
      list.push(facetObject["PageBytesFacet"]  == "None" ? "" : facetObject["PageBytesFacet"]);
      list.push(facetObject["PageNumberLinksFacet"] == "None" ? "" : facetObject["PageNumberLinksFacet"]);
      list.push(facetObject["PageLastModifiedFacet"]  == "None" ? "" : facetObject["PageLastModifiedFacet"]);
      list.push(facetObject["PageHasRedirectFacet"] == "None" ? "" : facetObject["PageHasRedirectFacet"]);
      console.log(list)
    let response;
    if(list.every(item => item === '')){
      response  = await fetch("http://localhost:5000/autonomous/get_pages/" + searchInput, {
        method: "GET"
    })
    } else {
      response = await fetch("http://localhost:5000/autonomous/get_pages_facets/", {
        method: "POST",
        body: JSON.stringify(list),
        headers: {
          "content-type": "application/json",
        },
      })
    }

    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
      
    const data = await response.json();
    console.log(data); // You can log or process the data here

    return data;

    } catch (error) {
      console.error("Error:", error);
      throw error; // Re-throw the error for the calling code to handle
    }
  }
export async function getAutonomousDocument(id){
    try{
      console.log(id)
      const response = await fetch("http://localhost:5000/autonomous/get_page/" + id, {
        method: "POST",
        headers: {
          "content-type": "application/json",
        },
      })
      
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      
      const data = await response.json();
      console.log(data); // You can log or process the data here
      return data[0];
    } catch (error) {
      console.error("Error:", error);
      throw error; // Re-throw the error for the calling code to handle
    }
}

export async function addSQLLike(id, vote){
  try {
    const response = await fetch("http://localhost:5000/autonomous/update_pagepoints/" + id , {
      method: "PUT",
      body: JSON.stringify({
        value: vote
      }),
      headers: {
        "content-type": "application/json",
      },
    });

    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    
    const data = await response.json();
    console.log(data); // You can log or process the data here
    return data;
  } catch (error) {
    console.error("Error:", error);
    throw error; // Re-throw the error for the calling code to handle
  }
}
