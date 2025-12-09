package com.nato1000.infiniteserver26

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.grid.GridCells
import androidx.compose.foundation.lazy.grid.LazyVerticalGrid
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.nato1000.infiniteserver26.ui.theme.InfiniteServer26Theme

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            InfiniteServer26Theme {
                Surface(
                    modifier = Modifier.fillMaxSize(),
                    color = MaterialTheme.colorScheme.background
                ) {
                    DashboardScreen()
                }
            }
        }
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun DashboardScreen() {
    var selectedTab by remember { mutableStateOf(0) }
    
    Scaffold(
        topBar = {
            TopAppBar(
                title = { 
                    Text(
                        "∞ Infinite Server26",
                        fontWeight = FontWeight.Bold
                    )
                },
                colors = TopAppBarDefaults.topAppBarColors(
                    containerColor = Color(0xFF141a2e),
                    titleContentColor = Color.White
                )
            )
        }
    ) { paddingValues ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(paddingValues)
                .padding(16.dp)
        ) {
            // Status Badge
            Card(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(bottom = 16.dp),
                colors = CardDefaults.cardColors(
                    containerColor = Color(0xFF141a2e)
                )
            ) {
                Row(
                    modifier = Modifier
                        .padding(16.dp)
                        .fillMaxWidth(),
                    horizontalArrangement = Arrangement.Center,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Text(
                        "🛡️ FORTRESS MODE ACTIVE",
                        color = Color(0xFF00ff41),
                        fontWeight = FontWeight.Bold,
                        fontSize = 18.sp
                    )
                }
            }
            
            // Metrics Grid
            LazyVerticalGrid(
                columns = GridCells.Fixed(2),
                horizontalArrangement = Arrangement.spacedBy(12.dp),
                verticalArrangement = Arrangement.spacedBy(12.dp),
                modifier = Modifier.fillMaxWidth()
            ) {
                item {
                    MetricCard(
                        icon = "⚡",
                        title = "CPU Usage",
                        value = "45%",
                        color = Color(0xFFffaa00)
                    )
                }
                item {
                    MetricCard(
                        icon = "💾",
                        title = "Memory",
                        value = "62%",
                        color = Color(0xFF00aaff)
                    )
                }
                item {
                    MetricCard(
                        icon = "🔒",
                        title = "Threats",
                        value = "0",
                        color = Color(0xFF00ff41)
                    )
                }
                item {
                    MetricCard(
                        icon = "🐳",
                        title = "Containers",
                        value = "8",
                        color = Color(0xFFaa00ff)
                    )
                }
            }
            
            Spacer(modifier = Modifier.height(24.dp))
            
            // AI Systems
            Text(
                "AI Systems Status",
                fontSize = 20.sp,
                fontWeight = FontWeight.Bold,
                color = Color.White,
                modifier = Modifier.padding(bottom = 12.dp)
            )
            
            LazyColumn(
                verticalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                item {
                    AISystemCard("NayDoeV1 Orchestrator", "AUTONOMOUS", true)
                }
                item {
                    AISystemCard("JessicAi Huntress", "NO MERCY MODE", true)
                }
                item {
                    AISystemCard("Quantum TwinBrain", "ENHANCED", true)
                }
                item {
                    AISystemCard("NAi_gAil Shield", "IMPENETRABLE", true)
                }
            }
        }
    }
}

@Composable
fun MetricCard(icon: String, title: String, value: String, color: Color) {
    Card(
        modifier = Modifier
            .fillMaxWidth()
            .height(120.dp),
        colors = CardDefaults.cardColors(
            containerColor = Color(0xFF141a2e)
        )
    ) {
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(16.dp),
            verticalArrangement = Arrangement.SpaceBetween
        ) {
            Text(
                icon,
                fontSize = 32.sp
            )
            Column {
                Text(
                    title,
                    fontSize = 12.sp,
                    color = Color.Gray
                )
                Text(
                    value,
                    fontSize = 24.sp,
                    fontWeight = FontWeight.Bold,
                    color = color
                )
            }
        }
    }
}

@Composable
fun AISystemCard(name: String, status: String, isOnline: Boolean) {
    Card(
        modifier = Modifier.fillMaxWidth(),
        colors = CardDefaults.cardColors(
            containerColor = Color(0xFF141a2e)
        )
    ) {
        Row(
            modifier = Modifier
                .padding(16.dp)
                .fillMaxWidth(),
            horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically
        ) {
            Row(
                verticalAlignment = Alignment.CenterVertically
            ) {
                Surface(
                    modifier = Modifier.size(8.dp),
                    shape = MaterialTheme.shapes.small,
                    color = if (isOnline) Color(0xFF00ff41) else Color.Red
                ) {}
                Spacer(modifier = Modifier.width(12.dp))
                Text(
                    name,
                    color = Color.White,
                    fontSize = 14.sp
                )
            }
            
            Surface(
                color = Color(0xFF00ff41).copy(alpha = 0.1f),
                shape = MaterialTheme.shapes.small
            ) {
                Text(
                    status,
                    color = Color(0xFF00ff41),
                    fontSize = 10.sp,
                    fontWeight = FontWeight.Bold,
                    modifier = Modifier.padding(horizontal = 8.dp, vertical = 4.dp)
                )
            }
        }
    }
}
