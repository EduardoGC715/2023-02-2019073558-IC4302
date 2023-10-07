
export async function getRegister(email, password, phone, name, last_name1, last_name2) {
  try {
    const response = await fetch("http://localhost:5000/register", {
      method: "POST",
      body: JSON.stringify({
        email,
        password,
        phone,
        name,
        last_name1,
        last_name2
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