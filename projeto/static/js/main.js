let chartTemp, chartUmid, chartPressao;

function iniciarGraficos() {
    const ctxTemp = document.getElementById('graficoTemp');
    if (!ctxTemp) return; // Se não estiver na home, não inicia

    const carregarGrafico = (ctx, label, cor) => {
        return new Chart(ctx, {
            type: 'line',
            data: { labels: [], datasets: [{ label: label, data: [], borderColor: cor, tension: 0.1 }] },
            options: { responsive: true, scales: { x: { display: false } } }
        });
    };

    chartTemp = carregarGrafico(ctxTemp, 'Temperatura (°C)', '#ff6384');
    chartUmid = carregarGrafico(document.getElementById('graficoUmid'), 'Umidade (%)', '#36a2eb');
    chartPressao = carregarGrafico(document.getElementById('graficoPressao'), 'Pressão (hPa)', '#4bc0c0');
}

function atualizarTudo() {
    fetch('/leituras')
        .then(res => res.json())
        .then(dados => {
            if (dados.length === 0) return;

            // 1. Inverte TODOS os dados para que o MAIS RECENTE seja o primeiro da lista
            const dadosRecentes = [...dados].reverse();

            // 2. Atualiza Gráficos
            if (chartTemp) {
                // Pega as 15 leituras mais recentes e inverte DE NOVO para o gráfico
                // ir da esquerda (passado) para a direita (presente)
                const dadosGrafico = dadosRecentes.slice(0, 15).reverse();
                const labels = dadosGrafico.map(d => d.timestamp.split(' ')[1]);
                
                chartTemp.data.labels = labels;
                chartTemp.data.datasets[0].data = dadosGrafico.map(d => d.temperatura);
                chartTemp.update();

                chartUmid.data.labels = labels;
                chartUmid.data.datasets[0].data = dadosGrafico.map(d => d.umidade);
                chartUmid.update();

                chartPressao.data.labels = labels;
                chartPressao.data.datasets[0].data = dadosGrafico.map(d => d.pressao);
                chartPressao.update();
            }

            // 3. Atualiza Tabela Dashboard (Os 10 mais recentes no topo)
            const corpoDash = document.getElementById("corpo-tabela-dashboard");
            if (corpoDash) {
                corpoDash.innerHTML = dadosRecentes.slice(0, 10).map(l => `
                    <tr>
                        <td>${l.timestamp}</td>
                        <td>${l.temperatura}°C</td>
                        <td>${l.umidade}%</td>
                        <td>${l.pressao || 'N/A'}</td>
                    </tr>
                `).join('');
            }

            // 4. Atualiza Tabela Histórico (Todos, do mais novo para o mais velho)
            const corpoHist = document.getElementById("corpo-tabela-historico");
            if (corpoHist) {
                corpoHist.innerHTML = dadosRecentes.map(l => `
                    <tr id="linha-${l.id}">
                        <td>${l.id}</td>
                        <td>${l.timestamp}</td>
                        <td>${l.temperatura}</td>
                        <td>${l.umidade}</td>
                        <td>${l.pressao || 'N/A'}</td>
                        <td>
                            <button onclick="window.location.href='/editar/${l.id}'" style="background:#ffc107; border:none; padding:5px 10px; cursor:pointer; border-radius: 3px;">Editar</button>
                            <button onclick="deletarLeitura(${l.id})" style="background:#ff4444; color:white; border:none; padding:5px 10px; cursor:pointer; border-radius: 3px; margin-left: 5px;">Excluir</button>
                        </td>
                    </tr>
                `).join('');
            }
        });
}

function deletarLeitura(id) {
    if (confirm("Deseja excluir?")) {
        fetch(`/leituras/${id}`, { method: 'DELETE' }).then(() => atualizarTudo());
    }
}

// Inicialização
document.addEventListener('DOMContentLoaded', () => {
    iniciarGraficos();
    atualizarTudo();
    setInterval(atualizarTudo, 5000); // Atualiza a cada 5 segundos
});