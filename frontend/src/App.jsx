import {useState, useEffect} from 'react'

function App() {
  const [tugasList, setTugasList] = useState([]) // state : daftar tugas
  const [judulBaru, setJudulBaru] = useState("") // state input dari tugas baru

  // ambil data api saat komponen pertama muncul
  useEffect(() => {
    fetch('http://localhost:8000/tasks')
      .then((res) => res.json())
      .then((data) => setTugasList(data))
  },[])

  // fungsi tambah tugas
  function tambahTugas(e) {
    e.preventDefault()
    fetch('http://localhost:8000/tasks', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({judul: judulBaru}),
    })
    .then((res) => res.json())
    .then((tugasBaru) => {
      setTugasList([...tugasList, tugasBaru])
      setJudulBaru('')
    })
  }
  
  function hapusTugas(id) {
    fetch('http://localhost:8000/tasks/' + id, {method: 'DELETE'})
      .then(() => setTugasList(tugasList.filter((tugas) => tugas.id !== id)))
      // .then(() => fetch('http://localhost:8000/tasks'))
      //   .then((res) => res.json())
      //   .then((data) => setTugasList(data))
  }

  // buat daftarnya (render)
  return  (
    <div>
      <h1>TakskFlow</h1>
      
      {/* form tambah tugas */}
      <form onSubmit={tambahTugas}>
        <input 
          value={judulBaru}
          onChange={(e) => setJudulBaru(e.target.value)}
          placeholder='Tugas Baru'
         />
         <button type="submit">Tambah</button>
      </form>

      {/* tampilan list tugas/tasks + delete */}
      <ul>
        {tugasList.map((tugas) => (
          <li key={tugas.id}>
            {tugas.judul} - {tugas.selesai ? "🟩" : "🟥"}
            <button onClick={() => hapusTugas(tugas.id)}>Hapus</button>
          </li>
        ))}
      </ul>
    </div>
  )
}

export default App