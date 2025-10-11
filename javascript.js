
// --- Constants & Utilities ---
const delay = ms => new Promise(res => setTimeout(res, ms));

const users = [
    { id: 1, name: "Alice", active: true },
    { id: 2, name: "Bob", active: false },
    { id: 3, name: "Charlie", active: true }
];

// --- Async Function with Fetch ---
async function fetchUserData(id) {
    console.log(`Fetching data for user ${id}...`);
    await delay(500); // fake delay
    return { email: `${id}@example.com`, lastLogin: new Date() };
}

// --- Main Logic ---
(async () => {
    const activeUsers = users.filter(u => u.active);

    for (const user of activeUsers) {
        const { id, name } = user;
        const data = await fetchUserData(id);

        const summary = {
            id,
            name,
            email: data.email,
            lastLogin: data.lastLogin.toISOString()
        };

        console.log(
            `👤 ${name} (${id})\n📧 ${summary.email}\n🕒 ${summary.lastLogin}\n`
        );
    }
})();
