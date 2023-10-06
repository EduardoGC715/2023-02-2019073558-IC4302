
export async function getLogin(email, password){
  try{
    const response = await fetch("http://localhost:5000/login", {
      method: "POST",
      body: JSON.stringify({
        email,
        password
      }),
      headers: {
        "content-type": "application/json",
      },
    })
    
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