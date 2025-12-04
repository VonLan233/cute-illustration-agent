import { useState, useEffect } from 'react'
import axios from 'axios'
import './App.css'

function App() {
  const [styles, setStyles] = useState([])
  const [sizes, setSizes] = useState([])
  const [selectedStyles, setSelectedStyles] = useState([])
  const [selectedSize, setSelectedSize] = useState('square_medium')
  const [theme, setTheme] = useState('')
  const [extraDescription, setExtraDescription] = useState('')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)
  const [healthStatus, setHealthStatus] = useState(null)

  // 加载风格和尺寸选项
  useEffect(() => {
    const fetchData = async () => {
      try {
        const [stylesRes, sizesRes, healthRes] = await Promise.all([
          axios.get('/api/v1/styles'),
          axios.get('/api/v1/sizes'),
          axios.get('/health')
        ])
        setStyles(stylesRes.data.styles)
        setSizes(sizesRes.data.sizes)
        setHealthStatus(healthRes.data.status)
      } catch (err) {
        setError('无法连接后端服务，请确保后端已启动')
        console.error(err)
      }
    }
    fetchData()
  }, [])

  // 切换风格选择
  const toggleStyle = (styleId) => {
    setSelectedStyles(prev =>
      prev.includes(styleId)
        ? prev.filter(s => s !== styleId)
        : [...prev, styleId]
    )
  }

  // 生成图片
  const handleGenerate = async () => {
    if (!theme.trim()) {
      setError('请输入主题描述')
      return
    }
    if (selectedStyles.length === 0) {
      setError('请至少选择一个风格')
      return
    }

    setLoading(true)
    setError(null)
    setResult(null)

    try {
      const response = await axios.post('/api/v1/generate', {
        theme: theme.trim(),
        styles: selectedStyles,
        size: selectedSize,
        extra_description: extraDescription.trim() || null,
        style_strength: 0.8
      })
      setResult(response.data)
    } catch (err) {
      setError(err.response?.data?.detail || '生成失败，请重试')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app-container">
      <h1>可爱插图生成智能体</h1>

      {/* 后端状态 */}
      <div className="status-bar">
        后端状态: {healthStatus === 'healthy' ? '✅ 已连接' : '❌ 未连接'}
      </div>

      {/* 主题输入 */}
      <div className="input-section">
        <label>主题描述 *</label>
        <input
          type="text"
          value={theme}
          onChange={(e) => setTheme(e.target.value)}
          placeholder="例如：一只猫咪戴着蝴蝶结"
          disabled={loading}
        />
      </div>

      {/* 风格选择 */}
      <div className="input-section">
        <label>选择风格 * (可多选)</label>
        <div className="style-grid">
          {styles.map(style => (
            <button
              key={style.id}
              className={`style-btn ${selectedStyles.includes(style.id) ? 'selected' : ''}`}
              onClick={() => toggleStyle(style.id)}
              disabled={loading}
            >
              {style.name}
            </button>
          ))}
        </div>
      </div>

      {/* 尺寸选择 */}
      <div className="input-section">
        <label>图片尺寸</label>
        <select
          value={selectedSize}
          onChange={(e) => setSelectedSize(e.target.value)}
          disabled={loading}
        >
          {sizes.map(size => (
            <option key={size.id} value={size.id}>
              {size.name} ({size.size})
            </option>
          ))}
        </select>
      </div>

      {/* 额外描述 */}
      <div className="input-section">
        <label>额外描述 (可选)</label>
        <textarea
          value={extraDescription}
          onChange={(e) => setExtraDescription(e.target.value)}
          placeholder="补充细节，如：在草地上玩耍，阳光明媚"
          disabled={loading}
        />
      </div>

      {/* 生成按钮 */}
      <button
        className="generate-btn"
        onClick={handleGenerate}
        disabled={loading || healthStatus !== 'healthy'}
      >
        {loading ? '生成中...' : '生成插图'}
      </button>

      {/* 错误提示 */}
      {error && <div className="error-msg">{error}</div>}

      {/* 生成结果 */}
      {result && (
        <div className="result-section">
          <h2>生成结果</h2>
          <div className="result-info">
            <p><strong>生成ID:</strong> {result.generation_id}</p>
            <p><strong>优化后的提示词:</strong></p>
            <pre>{result.optimized_prompt}</pre>
          </div>
          {result.image_url && (
            <div className="result-image">
              <img src={result.image_url} alt="生成的插图" />
            </div>
          )}
        </div>
      )}
    </div>
  )
}

export default App
