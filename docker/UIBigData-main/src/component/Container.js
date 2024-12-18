import React, { useEffect, useState } from 'react'
import defaultImg from '../static/images/OIP.jpg'
import { FcNext } from "react-icons/fc";

export default function Container({ page, setPage }) {
    const [textData, setTextData] = useState('');
    const [title, setTitle] = useState('')

    useEffect(() => {
        // Đọc file XML
        // fetch(page) // Đảm bảo file `example.xml` nằm trong thư mục `public`
        //     .then((response) => response.text())
        //     .then((data) => {
        //         // Phân tích cú pháp XML
        //         const parser = new DOMParser();
        //         const xmlDoc = parser.parseFromString(data, "text/xml");

        //         // Lấy tất cả các thẻ <text>
        //         const textNodes = xmlDoc.getElementsByTagName("text");
        //         const texts = Array.from(textNodes).map((node) => node.textContent.trim());kk
        //         setTextData(texts);

        //         // Lấy tất cả các thẻ <title>
        //         const titleNodes = xmlDoc.getElementsByTagName("title");
        //         const titles = Array.from(titleNodes).map((node) => node.textContent.trim());

        //         setTitle(titles)
        //     })
        //     .catch((err) => console.error("Error reading XML file:", err));
        setTitle(page?.title)
        setTextData(page?.text)
    }, [page]);

    // useEffect(() => {
    //     // Fetch dữ liệu từ tệp testdata.txt trong thư mục public
    //     fetch('/testdata.txt')
    //         .then((response) => response.text())
    //         .then((data) => setTextData(data));
    // }, []);

    return (
        <div style={{
            marginTop: 40,
            width: '1000px',
            display: 'flex'
        }}>
            <NavBarSite title={title} textData={textData} />
            <Content title={title} textData={textData} />
        </div>
    )
}

const NavBarSite = ({ title, textData }) => {
    const divideText = (text) => {
        text = String(text);
        let result = [{
            name: "(Top)",
            children: []
        }];

        const regex = /={2,4}[^=]+={2,4}/g;  // Tìm các cụm ==...==, ===...===, ====...====

        let match;

        while ((match = regex.exec(text)) !== null) {
            // Lấy matchText từ phần văn bản giữa dấu "=" và loại bỏ dấu "=" bao quanh
            const matchText = match[0].replace(/^=+|=+$/g, '').trim();  // Loại bỏ dấu "=" ở đầu và cuối
            if (!matchText) continue;  // Nếu không có văn bản hợp lệ thì bỏ qua

            const equalCount = match[0].match(/^=+/)[0].length;  // Đếm số dấu "=" trong chuỗi

            if (equalCount === 2) {
                // Đối với ==...==: tạo một phần tử cha mới
                const parentNode = {
                    name: matchText,
                    children: [],
                    open: false
                };
                result.push(parentNode);
            } else if (equalCount === 3) {
                // Đối với ===...===: tạo phần tử con dưới phần tử cha
                const childNode = {
                    name: matchText,
                    children: [],
                    open: false
                };
                let len = result.length
                result[len - 1].children.push(childNode);
            }
            else if (equalCount === 4) {
                // Đối với ====...====: có thể xử lý tương tự như ===...===
                const childNode = {
                    name: matchText
                };
                //result = [{==..==, children: [{===..===, children: []}]}]
                // let lenlv2 = result.length
                // let child2 = result[lenlv2 - 1].children
                // let lenlv3 = child2.length
                // let child3 = child2[lenlv3 - 1].children
                // let newChild3 = [...child3, childNode]
                // child2[lenlv3 - 1] = newChild3
                // result[lenlv2 - 1] = child2
                // result[lenlv2].children = newChild
            }
        }

        return result;
    };

    let [parts, setParts] = useState([]);
    useEffect(() => {
        setParts(divideText(textData));
    }, [textData]);

    const scrollToParagraph = (name) => {
        const target = document.getElementById(name);
        target?.scrollIntoView({
            behavior: 'smooth',  // Hiệu ứng cuộn mượt mà
            block: 'start',      // Đảm bảo thẻ P luôn ở đầu màn hình
        });
    };

    return (
        <div style={{
            width: '40%'
        }}>
            <div style={{
                position: 'fixed',
                width: '180px',
                fontSize: 14
            }}>
                {
                    parts.length > 0 && parts.map((item, index) => {
                        return (
                            <div key={index} style={{ marginBottom: 10, display: 'flex', alignItems: 'baseline' }}>
                                {
                                    item.children.length > 0 ? <div onClick={() => {
                                        setParts(prev => {
                                            let updateItem = [...prev]
                                            updateItem[index] = { ...updateItem[index], "open": !prev[index].open }
                                            return updateItem
                                        })
                                    }}
                                        style={{ width: 20, height: 20, display: 'flex', justifyContent: 'flex-start', alignItems: 'center', cursor: 'pointer', color: "#283ec7" }}><FcNext /></div>
                                        : <div style={{ width: 20, height: 20 }}> </div>
                                }
                                <div>
                                    <a href={'_' + item.name.replace(/\s+/g, '_').replace(/[^\w\-]/g, '') + '_'}
                                        onClick={(e) => {
                                            e.preventDefault();
                                            item.name === "(Top)" ? scrollToParagraph(title) :
                                                scrollToParagraph('_' + item.name.replace(/\s+/g, '_').replace(/[^\w\-]/g, '') + '_')
                                        }
                                        }
                                        style={{ textDecoration: 'none' }}>
                                        {item.name}
                                    </a>
                                    {
                                        item.open && item.children.length > 0 && item.children.map((i, id) => {
                                            return (
                                                <div key={index + '.' + id} style={{ padding: 5, marginLeft: 20 }}>
                                                    <a href={'_' + i.name.replace(/\s+/g, '_').replace(/[^\w\-]/g, '') + '_'}
                                                        onClick={(e) => {
                                                            e.preventDefault();
                                                            scrollToParagraph('_' + i.name.replace(/\s+/g, '_').replace(/[^\w\-]/g, '') + '_')
                                                        }
                                                        }
                                                        style={{ textDecoration: 'none' }}>{i.name}</a>
                                                </div>
                                            )
                                        })
                                    }
                                </div>
                            </div>
                        )
                    })
                }
            </div>
        </div>
    )
}

const Content = ({ title, textData }) => {
    // Hàm xử lý văn bản
    const processText = (text) => {
        // Thay thế các từ trong cặp ''' ''' thành thẻ <strong> (in đậm)
        text = text.replace(/'''([^']+)'''/g, '<strong>$1</strong>');

        //Thay mấy cái dạng {{Sfnm|1a1=Merriam-Webster|1y=2019|1loc="Anarchism"|2a1=''Oxford English Dictionary''|2y=2005|2loc="Anarchism"|3a1=Sylvan|3y=2007|3p=260}}
        text = text.replace(/{{([^}]+)}}/g, (match, p1, index) => {
            if (p1.includes("Main|")) {
                // Chia chuỗi tại dấu "|" và lấy phần sau dấu "|"
                const parts = p1.split('|');
                return `<i style="margin-left: 20px; line-height: 1.5;">Main article: <a href="#" style="color: #283ec7; text-decoration: none;">${parts[1]}</a></i>`;
            } else if (p1.includes("See also|")) {
                // Chia chuỗi tại dấu "|" và lấy phần sau dấu "|"
                const parts = p1.split('|');
                return `<i style="margin-left: 20px; line-height: 1.5;">See also: <a href="#" style="color: #283ec7; text-decoration: none;">${parts[1]}</a></i>`;
            }
            else {
                // Nếu không có "Main" hoặc "See also", trả về số lượng phần tử
                // const parts = p1.split('|');
                // return `<a href="#" style="font-size: 13px; color: #283ec7; text-decoration: none; :hover {text-decoration: underline}">[${parts.length}]</a>`;
                return `<span></span>`
            }
        });

        //Xử lý bảng //xóa bố bảng đi, không nói nhiều
        // text = text.replace(/\{\|[^|]*\|}/g, '');
        //     .replace(/&quot;/g, '"')       // Thay &quot; thành "
        //     .replace(/&lt;/g, '<')         // Thay &lt; thành <
        //     .replace(/&gt;/g, '>')         // Thay &gt; thành >
        //     .replace(/\{\|/g, '<table') // Mở thẻ <table>
        //     .replace(/\|\+/g, '<caption>') // Chuyển \|+ thành <caption>
        //     .replace(/\|\-/g, '<tr')      // Chuyển \|- thành <tr>
        //     .replace(/\!\s*scope="col"/g, 'scope="col"')
        //     .replace()

        // .replace(/<tr>\|([^|]+)\|\|([^|]+)\|\|([^|]+)\|<tr>/g,
        //     '<tr><td>$1</td><td>$2</td><td>$3</td></tr><tr>'
        // )
        // .replace(/\!\s*scope="col"\|/g, '<th scope="col">') // Chuyển !scope="col" thành <th scope="col">
        // .replace(/\|}/g, '</table>')   // Đóng thẻ </table>
        // .replace(/<br\/>/g, '<br>')    // Thay <br/> thành <br>
        // .replace(/\{\{Small\|/g, '')   // Xóa phần text {{Small|
        // .replace(/\{\{Sfn\|Kinna\|2019\|p=97\}\}\}\}/g, '') // Xóa citation không cần thiết
        // .replace(/<\/caption>/,
        //     '<br><span style="font-size:85%;">Ruth Kinna (2019)<sup id="cite_ref-FOOTNOTEKinna201997_162-0" class="reference"><a href="#cite_note-FOOTNOTEKinna201997-162"><span class="cite-bracket">[</span>159<span class="cite-bracket">]</span></a></sup></span></caption>'
        // )

        // Thay thế các từ trong === === thành thẻ span với phong cách đặc biệt
        text = text.replace(/====([^=]+)====/g, (match, p1) => {
            // Làm sạch nội dung để làm ID hợp lệ (thay thế dấu cách bằng dấu gạch dưới, loại bỏ các ký tự đặc biệt)
            const validId = p1.replace(/\s+/g, '_').replace(/[^\w\-]/g, '');

            // let len = navbar.length
            // const newItem = [...navbar[len - 1], p1]
            // let updateNavbar = [...navbar]
            // updateNavbar[len - 1] = newItem
            // setNavbar(updateNavbar)

            return `<p id="${validId}" style="font-size: 17px; font-weight: bold; color: 'black';">${p1}</p>`;
        });

        // Thay thế các từ trong === === thành thẻ span với phong cách đặc biệt
        text = text.replace(/===([^=]+)===/g, (match, p1) => {
            // Làm sạch nội dung để làm ID hợp lệ (thay thế dấu cách bằng dấu gạch dưới, loại bỏ các ký tự đặc biệt)
            const validId = p1.replace(/\s+/g, '_').replace(/[^\w\-]/g, '');

            // let len = navbar.length
            // const newItem = [...navbar[len - 1], p1]
            // let updateNavbar = [...navbar]
            // updateNavbar[len - 1] = newItem
            // setNavbar(updateNavbar)

            return `<p id="${validId}" style="font-size: 20px; font-weight: bold; color: 'black';">${p1}</p>`;
        });

        // Thay thế các từ trong == == thành thẻ span với phong cách đặc biệt
        text = text.replace(/==([^=]+)==/g, (match, p1) => {
            // Làm sạch nội dung để làm ID hợp lệ (thay thế dấu cách bằng dấu gạch dưới, loại bỏ các ký tự đặc biệt)
            const validId = p1.replace(/\s+/g, '_').replace(/[^\w\-]/g, '');

            // setNavbar([...navbar, p1])

            return `<p id="${validId}" style="color: 'black'; font-size: 28px; font-weight: 400; border-bottom: 1px solid gray; padding-bottom: 10px; font-family: 'Times New Roman', Times, serif;">${p1}</p>`;
        });

        //Thay nội dung trong cặp '' '' bằng chữ nghiêng trong văn bản
        text = text.replace(/''([^']+)''/g, (match, p1) => {
            return `<i>${p1}</i>`;
        });



        // Thay thế các từ trong [[ ]] thành thẻ <a>
        // text = text.replace(/\[\[([^\]]+)\]\]/g, (match, p1) => {
        //     // Kiểm tra nếu p1 chứa dấu "|", nếu có thì lấy phần sau dấu "|"
        //     const displayText = p1.includes('|') ? p1.split('|')[1] : p1;

        //     return `<a href="#" style="color: #283ec7; text-decoration: none">${displayText}</a>`;
        // });
        text = text.replace(/\[\[([^\[\]]+)\]\]/g, (match, p1) => {
            if (p1.startsWith('File:')) {
                return match;  // Trả về match ban đầu (không thay đổi nếu là "File:")
            }
            // Kiểm tra nếu p1 chứa dấu "|", nếu có thì lấy phần sau dấu "|"
            const displayText = p1.includes('|') ? p1.split('|')[1] : p1;

            return `<a href="#" style="color: #283ec7; text-decoration: none">${displayText}</a>`;
        });

        //Xử lý xuống dòng
        text = text.replace(/\n/g, '<br>');


        text = text.replace(/\[\[File:([^\|]+)\|thumb\|([^\]]+)\]\]/g, (match, p1, p2) => {
            const displayText = p2.includes("|") ? p2.split('|')[1] : p2;
            return `
                <div style="margin-bottom: 20px; margin-left: 10px; width: 230px; border: 2px solid #ccc; background-color: #ccc;float: right;">
                    <img src="${defaultImg}" alt="${p1}" style="object-fit: cover; width: 100%; " />
                    <p style="margin: 10px; ">${displayText}</p>
                </div>
            `;
        });

        //Xử lý ảnh thumb
        text = text.replace(/\[\[File:([^\|]+)\|thumb\|([^\]]+)\]\]/g, (match, p1, p2) => {
            return `
                <div style="margin-bottom: 20px; margin-left: 10px; width: 230px; border: 2px solid #ccc; background-color: #ccc;float: right; ">
                    <img src="${defaultImg}" alt="${p1}" style="object-fit: cover; width: 100%;" />
                    <p style="margin: 10px; ">${p2}</p>
                </div>
            `;
        });

        text = text.replace(/\{\|[\s\S]*\|\}/g, '');

        return text;
    };

    // const divideText = (text) => {
    //     text = String(text)
    //     const result = [];
    //     const regexEqual = /==[^=]+==[^=]/g;  // Tìm các cụm == ... == (không phải ===)

    //     let lastIndex = 0;
    //     let match;

    //     // Duyệt qua các kết quả khớp với regex cho cụm == ... == (không phải ===)
    //     while ((match = regexEqual.exec(text)) !== null) {
    //         // Phần văn bản trước cụm == ... ==, nếu có
    //         if (match.index > lastIndex) {
    //             result.push(text.slice(lastIndex, match.index).trim());
    //         }
    //         // Thêm phần cụm == ... == vào kết quả
    //         result.push(text.slice(match.index, regexEqual.lastIndex).trim());
    //         lastIndex = regexEqual.lastIndex;
    //     }

    //     // Thêm phần văn bản còn lại sau tất cả các cụm == ... ==, nếu có
    //     if (lastIndex < text.length) {
    //         result.push(text.slice(lastIndex).trim());
    //     }

    //     return result;
    // };

    return (
        <div style={{
            witdth: '60%'
        }}>
            <div style={{ width: '800px' }}>
                <p id={title}
                    style={{ color: 'black', borderBottomWidth: 1, borderBottomStyle: 'solid', borderColor: 'gray', fontSize: 30, fontFamily: 'Times New Roman, Times, serif' }}>
                    {title}
                </p>
                <div dangerouslySetInnerHTML={{ __html: processText(String(textData)) }} style={{ marginTop: 20, borderWidth: 1 }} />
            </div>
        </div>
    )
}
