<div class="highlight"><pre><span class="go">Python 2.6.1 (r261:67515, Jul  7 2009, 23:51:51) </span>
<span class="go">[GCC 4.2.1 (Apple Inc. build 5646)] on darwin</span>
<span class="go">Type &quot;help&quot;, &quot;copyright&quot;, &quot;credits&quot; or &quot;license&quot; for more information.</span>
<span class="gp">&gt;&gt;&gt; </span><span class="kn">import</span> <span class="nn">montage</span>
<span class="gp">&gt;&gt;&gt; </span><span class="n">montage</span><span class="o">.</span><span class="n">mArchiveList</span><span class="p">(</span><span class="s">&#39;2MASS&#39;</span><span class="p">,</span> <span class="s">&#39;K&#39;</span><span class="p">,</span> <span class="s">&#39;m31&#39;</span><span class="p">,</span> <span class="mf">0.5</span><span class="p">,</span> <span class="mf">0.5</span><span class="p">,</span> <span class="s">&#39;m31_list.tbl&#39;</span><span class="p">)</span>
<span class="go">count : 18</span>
<span class="go">stat : OK</span>
<span class="gp">&gt;&gt;&gt; </span><span class="n">montage</span><span class="o">.</span><span class="n">mMakeHdr</span><span class="p">(</span><span class="s">&#39;m31_list.tbl&#39;</span><span class="p">,</span> <span class="s">&#39;header.hdr&#39;</span><span class="p">,</span> <span class="n">north_aligned</span><span class="o">=</span><span class="bp">True</span><span class="p">)</span>
<span class="go">count : 18</span>
<span class="go">lat4 : 41.744136</span>
<span class="go">stat : OK</span>
<span class="go">lat1 : 40.912238</span>
<span class="go">lat3 : 41.744136</span>
<span class="go">latsize : 0.831951</span>
<span class="go">clon : 10.717965</span>
<span class="go">lonsize : 0.830562</span>
<span class="go">posang : 0.0</span>
<span class="go">lon4 : 11.274528</span>
<span class="go">lat2 : 40.912238</span>
<span class="go">lon1 : 11.267467</span>
<span class="go">clat : 41.32951</span>
<span class="go">lon2 : 10.168464</span>
<span class="go">lon3 : 10.161403</span>
<span class="gp">&gt;&gt;&gt; </span><span class="n">s</span> <span class="o">=</span> <span class="n">montage</span><span class="o">.</span><span class="n">mMakeHdr</span><span class="p">(</span><span class="s">&#39;m31_list.tbl&#39;</span><span class="p">,</span> <span class="s">&#39;header.hdr&#39;</span><span class="p">,</span> <span class="n">north_aligned</span><span class="o">=</span><span class="bp">True</span><span class="p">)</span>
<span class="gp">&gt;&gt;&gt; </span><span class="n">s</span><span class="o">.</span><span class="n">stat</span>
<span class="go">&#39;OK&#39;</span>
<span class="gp">&gt;&gt;&gt; </span><span class="n">s</span><span class="o">.</span><span class="n">lon1</span>
<span class="go">11.267467</span>
</pre></div>
