
#if defined(SHADER_STAGE_VS)

/*void main(uint x : SV_VertexID, out float4 posh : SV_Position, out float2 texc : TEXCOORD0){
	texc = float2((x<<1)&2,x&2);
	posh = float4(texc*float2(2,-2)+float2(-1,1),0,1);
}*/

float2 main(uint x : SV_VertexID) : POSITION0{
	return float2(0,0);
}

#elif defined(SHADER_STAGE_GS)

const float2 vertexPositions[4] = {
	float2(0.0f,0.0f),
	float2(1.0f,0.0f),
	float2(0.0f,1.0f),
	float2(1.0f,1.0f)
};

struct GS_OUTPUT{
	float4 posh : SV_Position;
	float2 texc : TEXCOORD;
};

//https://developer.nvidia.com/vulkan-shader-resource-binding
//https://www.khronos.org/assets/uploads/developers/library/2018-gdc-webgl-and-gltf/2-Vulkan-HLSL-There-and-Back-Again_Mar18.pdf
[[vk::push_constant]] cbuffer cb{
	float2 xy0;
	float2 xy1;
};

const float2 vertices[4] = {
	xy0,
	float2(xy1.x,xy0.y),
	float2(xy0.x,xy1.y),
	xy1
};

[maxvertexcount(4)]
//void main(point GS_INTPUT input[1], inout TriangleStream<GS_OUTPUT> stream){
void main(point float2 posh[1], inout TriangleStream<GS_OUTPUT> stream){
	GS_OUTPUT output;
	[unroll]
	for(uint i = 0; i < 4; ++i){
		output.posh = float4(vertices[i],0,1);
		output.texc = vertexPositions[i]; //TODO: should be adjusted according to dimensions of the box. Push constants need the maximum known border width
		stream.Append(output);
	}
	stream.RestartStrip();
}

#elif defined(SHADER_STAGE_PS)

[[vk::binding(0)]] Texture2D<float4> content;
[[vk::binding(1)]] SamplerState sm;

[[vk::push_constant]] cbuffer cb{
	float2 xy0;
	float2 xy1;
	float2 screen;
	float2 params;
};

//TODO: create chamfer with ndc coords and sdf transformation
float4 main(float4 posh : SV_Position, float2 texc : TEXCOORD0) : SV_Target{
	if(any(texc < 0.005) || any(texc > 0.995))
		return float4(0.5f+0.5f*sin(params.x),1,0,1);
	//float4 c = content.Sample(sm,texc);
	float2 p = screen*(0.5f*xy0+0.5f);
	float4 c = content.Load(float3(posh.xy-p,0)); //p already has the 0.5f offset
	c.w = 1.0f;
	return c;
#if 0
	float2 s = saturate(abs(2.0f*(xy1-xy0))); //reference
	float2 ct = 2.0f*texc-1.0f;
	ct = s*ct+sign(ct)*(1-s); //TODO: aspect ratio check, 1.0f/0.5f
	if(length(max(abs(ct)-1.2*float2(0.5,0.5),0.0f))-0.4f > 0.0f)
		discard;
	/*float2 ct = 0.5f*(xy0+xy1);
	if(length(max(abs(posh.xy+xy0)-float2(0.5,0.5),0.0f))-0.4f > 0.0f)
		discard;*/
	
	return float4(1,1,1,1);
#endif
}

#endif
